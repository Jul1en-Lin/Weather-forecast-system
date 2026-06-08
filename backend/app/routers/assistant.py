import logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Any, List, Optional, Sequence
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from app.data.tarot_cards import TAROT_CARD_IDS, TAROT_CARD_META

logger = logging.getLogger(__name__)

_WEEKDAY_MAP = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
DEFAULT_KNOWLEDGE_BASE_IDS = ["kb_weather", "kb_alert"]
WEATHER_TOOL_KEYWORDS = [
    "天气", "气温", "温度", "下雨", "降雨", "降水", "预报", "湿度", "风力", "风向",
    "空气质量", "pm2.5", "出行", "穿衣", "冷不冷", "热不热",
]
ALERT_TOOL_KEYWORDS = ["预警", "警报", "告警", "气象灾害", "台风", "暴雨", "高温", "寒潮", "雷雨大风", "冰雹"]
WEATHER_ORACLE_MODEL_PREFERENCE = ("mimo-v2.5", "MiniMax-M2.5")
from app.dependencies import get_db_session, get_current_user
from app.services.conversation import ConversationService
from app.services.llm import get_llm, stream_llm_response, strip_thinking_tags, ThinkingFilter, get_model_config
from app.services.knowledge_base import KnowledgeBaseService
from app.services.weather_tool import WeatherToolService
from app.core.sse import sse_response, SSEStream
from app.database import SessionLocal
from app.schemas.assistant import (
    ModelsResponse, ModelInfo,
    KnowledgeBasesResponse, KnowledgeBaseInfo,
    ToolsResponse, ToolInfo,
    ChatStreamRequest,
    WeatherCardRequest, WeatherCardResponse,
)
from app.schemas.conversation import (
    ConversationsResponse, ConversationItem,
    ConversationDetail, MessageItem,
    CreateConversationRequest, RenameConversationRequest,
    BatchDeleteRequest,
)

router = APIRouter(prefix="/api/v1/assistant", tags=["assistant"])

def resolve_knowledge_base_ids(knowledge_base_ids: Optional[List[str]]) -> List[str]:
    return knowledge_base_ids or DEFAULT_KNOWLEDGE_BASE_IDS.copy()

def resolve_tool_ids(
    message: str,
    supports_tools: bool,
    requested_tool_ids: Optional[List[str]] = None,
) -> List[str]:
    if not supports_tools:
        return []
    if requested_tool_ids:
        return requested_tool_ids

    normalized = message.lower()
    tool_ids: List[str] = []
    if any(keyword in normalized for keyword in WEATHER_TOOL_KEYWORDS):
        tool_ids.append("weather_query")
    if any(keyword in normalized for keyword in ALERT_TOOL_KEYWORDS):
        tool_ids.append("alert_query")
    return tool_ids


def clean_json_object_text(content: str) -> str:
    text = strip_thinking_tags(content or "").strip()
    if text.startswith("```"):
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            return text[start:end + 1]
    return text


def build_weather_fingerprint(weather: dict) -> str:
    return "|".join(
        [
            str(weather.get("temperature")),
            str(weather.get("humidity")),
            str(weather.get("pressure")),
            str(weather.get("wind_speed")),
            str(weather.get("condition")),
        ]
    )


def select_tarot_card_id(subject_key: str, date_key: str, weather_fingerprint: str = "") -> str:
    import hashlib

    seed = f"{subject_key}|{date_key}".encode("utf-8")
    digest = hashlib.sha256(seed).hexdigest()
    index = int(digest[:8], 16) % len(TAROT_CARD_IDS)
    return TAROT_CARD_IDS[index]


def select_preferred_weather_oracle_model_id(models: Sequence[object]) -> Optional[str]:
    for preferred_id in WEATHER_ORACLE_MODEL_PREFERENCE:
        if any(getattr(model, "id", None) == preferred_id for model in models):
            return preferred_id
    first_model = next(iter(models), None)
    return getattr(first_model, "id", None)


def format_weather_metric_value(value, unit: str = "") -> str:
    if value is None:
        return "未知"
    return f"{value}{unit}"


def non_empty_text(value: Any) -> Optional[str]:
    if isinstance(value, str):
        text = value.strip()
        return text or None
    return None


def parse_int_or_default(value: Any, default: int) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError:
            return default
    return default


def strip_metric_prefix(value: str) -> str:
    text = value.strip()
    for separator in ("：", ":"):
        if separator in text:
            suffix = text.split(separator, 1)[1].strip()
            if suffix:
                return suffix
    return text


def build_weather_daily_advice(weather: dict) -> dict:
    temperature = weather.get("temperature")
    humidity = weather.get("humidity")
    wind_speed = weather.get("wind_speed")
    condition = str(weather.get("condition") or "")

    rainy_keywords = ("雨", "雷", "阵雨", "降水")
    snowy_keywords = ("雪", "冻雨")
    hot = isinstance(temperature, (int, float)) and temperature >= 30
    warm = isinstance(temperature, (int, float)) and 24 <= temperature < 30
    mild = isinstance(temperature, (int, float)) and 20 <= temperature < 24
    cool = isinstance(temperature, (int, float)) and 12 <= temperature < 20
    cold = isinstance(temperature, (int, float)) and temperature < 12
    humid = isinstance(humidity, (int, float)) and humidity >= 80
    windy = isinstance(wind_speed, (int, float)) and wind_speed >= 25

    if any(keyword in condition for keyword in rainy_keywords):
        travel = "带伞出门，地面湿滑时别赶路。"
    elif any(keyword in condition for keyword in snowy_keywords):
        travel = "路面容易滑，通勤多留十分钟。"
    elif hot:
        travel = "中午少晒，外出带水和防晒。"
    elif windy:
        travel = "风比较大，骑车慢一点，帽子别戴太松。"
    else:
        travel = "正常出门就行，早晚留意临近预报。"

    if cold:
        clothing = "厚外套安排上，怕冷就加围巾。"
    elif cool:
        clothing = "长袖配薄外套，早晚别只穿短袖。"
    elif hot and humid:
        clothing = "穿透气短袖，少选闷汗面料。"
    elif hot:
        clothing = "短袖够用，外出加防晒衣或帽子。"
    elif warm:
        clothing = "短袖或薄衬衫，空调房备薄外套。"
    elif mild:
        clothing = "长袖或薄外套更合适，早晚别穿太少。"
    else:
        clothing = "穿日常衣物即可，怕冷就加一件薄外套。"

    return {"travel": travel, "clothing": clothing}


def normalize_daily_advice(raw_advice: Any, fallback: dict) -> dict:
    daily_advice = dict(fallback)
    if isinstance(raw_advice, dict):
        travel = (
            non_empty_text(raw_advice.get("travel"))
            or non_empty_text(raw_advice.get("travel_advice"))
            or non_empty_text(raw_advice.get("outdoor"))
            or non_empty_text(raw_advice.get("出行"))
            or non_empty_text(raw_advice.get("出行建议"))
        )
        clothing = (
            non_empty_text(raw_advice.get("clothing"))
            or non_empty_text(raw_advice.get("clothing_advice"))
            or non_empty_text(raw_advice.get("dress"))
            or non_empty_text(raw_advice.get("穿衣"))
            or non_empty_text(raw_advice.get("穿衣建议"))
        )
        if travel:
            daily_advice["travel"] = travel
        if clothing:
            daily_advice["clothing"] = clothing
    else:
        text = non_empty_text(raw_advice)
        if text:
            daily_advice["travel"] = text
    return daily_advice


def normalize_weather_oracle_model_data(card_data: dict, fallback: dict) -> dict:
    raw_fortune = card_data.get("fortune")
    fortune = dict(fallback["fortune"])
    if isinstance(raw_fortune, dict):
        for key in ("title", "summary", "lucky_color", "good_for", "avoid"):
            text = non_empty_text(raw_fortune.get(key))
            if text:
                fortune[key] = text
        fortune["lucky_number"] = parse_int_or_default(
            raw_fortune.get("lucky_number"),
            fortune["lucky_number"],
        )
    else:
        summary = non_empty_text(raw_fortune)
        if summary:
            fortune["summary"] = summary

    raw_mood = card_data.get("mood_guide")
    mood_guide = dict(fallback["mood_guide"])
    if isinstance(raw_mood, dict):
        for key in ("title", "analysis"):
            text = non_empty_text(raw_mood.get(key))
            if text:
                mood_guide[key] = text
        suggestions = raw_mood.get("suggestions")
        if isinstance(suggestions, list):
            normalized_suggestions = [
                item.strip()
                for item in suggestions
                if isinstance(item, str) and item.strip()
            ]
            if normalized_suggestions:
                mood_guide["suggestions"] = normalized_suggestions
        else:
            suggestion = non_empty_text(suggestions)
            if suggestion:
                mood_guide["suggestions"] = [suggestion]
    else:
        analysis = non_empty_text(raw_mood)
        if analysis:
            mood_guide["analysis"] = analysis

    raw_mappings = card_data.get("weather_mappings")
    weather_mappings = [dict(item) for item in fallback["weather_mappings"]]
    mapping_by_metric = {item["metric"]: item for item in weather_mappings}

    if isinstance(raw_mappings, dict):
        for metric, item in mapping_by_metric.items():
            raw_value = raw_mappings.get(metric) or raw_mappings.get(item["label"])
            if isinstance(raw_value, dict):
                for key in ("label", "value", "reading"):
                    text = non_empty_text(raw_value.get(key))
                    if text:
                        item[key] = text
                item["score"] = parse_int_or_default(raw_value.get("score"), item["score"])
            else:
                text = non_empty_text(raw_value)
                if text:
                    item["reading"] = strip_metric_prefix(text)
    elif isinstance(raw_mappings, list):
        for index, raw_item in enumerate(raw_mappings):
            if not isinstance(raw_item, dict):
                continue
            metric = non_empty_text(raw_item.get("metric"))
            if not metric and index < len(weather_mappings):
                metric = weather_mappings[index]["metric"]
            if not metric or metric not in mapping_by_metric:
                continue
            item = mapping_by_metric[metric]
            for key in ("label", "value", "reading"):
                text = non_empty_text(raw_item.get(key))
                if text:
                    item[key] = text
            item["score"] = parse_int_or_default(raw_item.get("score"), item["score"])

    daily_advice = normalize_daily_advice(
        card_data.get("daily_advice") or card_data.get("advice"),
        fallback["daily_advice"],
    )

    return {
        "fortune": fortune,
        "mood_guide": mood_guide,
        "daily_advice": daily_advice,
        "weather_mappings": weather_mappings,
    }


def build_weather_oracle_prompt(weather: dict, date_key: str, tarot: dict) -> str:
    import json

    weather_payload = {
        "condition": weather.get("condition"),
        "temperature": weather.get("temperature"),
        "humidity": weather.get("humidity"),
        "wind_speed": weather.get("wind_speed"),
    }
    card_payload = {
        "name_zh": tarot.get("name_zh"),
        "name_en": tarot.get("name_en"),
        "keywords": tarot.get("keywords"),
        "core_meaning": tarot.get("core_meaning"),
        "weather_oracle_hint": tarot.get("weather_oracle_hint"),
    }
    return (
        "只输出 JSON，不要 markdown。"
        f"日期={date_key};天气={json.dumps(weather_payload, ensure_ascii=False)};"
        f"塔罗={json.dumps(card_payload, ensure_ascii=False)};"
        "生成 fortune={title,summary,lucky_color,lucky_number,good_for,avoid}"
        " 和 mood_guide={title,analysis,suggestions}。"
    )

# ---- 模型列表 ----
@router.get("/models", response_model=ModelsResponse)
def get_models(db: Session = Depends(get_db_session)):
    from app.models.model_config import ModelConfig
    models_db = db.query(ModelConfig).order_by(ModelConfig.created_at.asc()).all()
    return ModelsResponse(models=[
        ModelInfo(
            id=m.id,
            name=m.name,
            description=m.description or ""
        ) for m in models_db
    ])

# ---- 知识库列表 ----
@router.get("/knowledge-bases", response_model=KnowledgeBasesResponse)
def get_knowledge_bases():
    return KnowledgeBasesResponse(knowledge_bases=[
        KnowledgeBaseInfo(id="kb_weather", name="气象术语库", description="气象专业术语释义"),
        KnowledgeBaseInfo(id="kb_alert", name="预警信号库", description="气象预警信号标准与防御指南"),
    ])

# ---- 工具列表 ----
@router.get("/tools", response_model=ToolsResponse)
def get_tools():
    return ToolsResponse(tools=[
        ToolInfo(id="weather_query", name="天气查询", description="查询实时天气信息"),
        ToolInfo(id="alert_query", name="预警查询", description="查询气象预警信号"),
    ])

# ---- 流式对话（核心） ----
# 注意：/chat/stream 必须放在 /conversations/{conversation_id} 之前，避免路径参数冲突
@router.post("/chat/stream")
async def chat_stream(
    req: ChatStreamRequest,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["user_id"]

    if req.conversation_id:
        conv = ConversationService.get(db, req.conversation_id, user_id)
        if not conv:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
        # 自动同步更新会话的 model_id，确保模型变更被持久化保存
        if conv.model_id != req.model_id:
            conv.model_id = req.model_id
            db.commit()
    else:
        conv = ConversationService.create(db, user_id, req.message[:30], req.model_id)

    conversation_id = conv.id
    ConversationService.add_message(db, conversation_id, "user", req.message)
    history_msgs = ConversationService.get_messages(db, conversation_id, user_id)

    now = datetime.now()
    weekday = _WEEKDAY_MAP[now.weekday()]
    date_str = f"今天是 {now.year} 年 {now.month} 月 {now.day} 日，{weekday}。"

    system_parts = [
        "你是一个专业的气象智能助手，帮助用户解答气象相关问题。",
        "【重要指令】无论用户是否主动提及出行，你必须始终在回答的末尾或合适位置，基于当前的天气状况（如温度、降水、风力、空气质量、预警等）提供具体、实用的出行建议（例如穿衣、是否需要携带雨具、防晒防寒、户外运动适宜度等）。",
        date_str,
    ]
    effective_knowledge_base_ids = resolve_knowledge_base_ids(req.knowledge_base_ids)
    config = get_model_config(req.model_id, db)
    supports_tools = config.get("supports_tools", True)
    effective_tool_ids = resolve_tool_ids(req.message, supports_tools, req.tool_ids)

    kb_context = KnowledgeBaseService.build_context(db, effective_knowledge_base_ids)
    if kb_context:
        system_parts.append("以下是相关气象知识库内容，请结合这些内容回答：\n" + kb_context)
    if "weather_query" in effective_tool_ids:
        system_parts.append("用户正在询问实时天气或天气预报，请调用 weather_query 工具获取结果后再回答。")
    if "alert_query" in effective_tool_ids:
        system_parts.append("用户正在询问实时气象预警，请调用 alert_query 工具获取结果后再回答。")

    if req.tool_ids and not supports_tools:
        tool_descs = []
        if "weather_query" in req.tool_ids:
            tool_descs.append("- 天气查询工具：可查询指定地区的实时天气信息")
        if "alert_query" in req.tool_ids:
            tool_descs.append("- 预警查询工具：可查询指定地区的实时气象预警信号")
        if tool_descs:
            system_parts.append("你可以参考以下工具信息来回答，但请基于你的知识直接回复（当前模型不支持自动调用外部工具）：\n" + "\n".join(tool_descs))

    lc_messages = [SystemMessage(content="\n".join(system_parts))]
    for m in history_msgs[:-1]:
        if m.role == "user":
            lc_messages.append(HumanMessage(content=m.content))
        elif m.role == "assistant":
            lc_messages.append(AIMessage(content=m.content))
    lc_messages.append(HumanMessage(content=req.message))

    tools = []
    tool_service = None
    alert_tool = None
    if effective_tool_ids:
        if "weather_query" in effective_tool_ids:
            tool_service = WeatherToolService.get_tool()
            if tool_service:
                tools.append(tool_service)
        if "alert_query" in effective_tool_ids:
            alert_tool = WeatherToolService.get_alert_tool()
            if alert_tool:
                tools.append(alert_tool)

    async def event_generator():
        assistant_content = ""
        try:
            llm = get_llm(req.model_id, streaming=True, db=db)
            if tools and supports_tools:
                bound_llm = llm.bind_tools(tools)
                first_response = await bound_llm.ainvoke(lc_messages)
                tool_calls = first_response.tool_calls if hasattr(first_response, "tool_calls") else []

                if tool_calls:
                    tool_messages = []
                    for tc in tool_calls:
                        tool_name = tc.get("name", "")
                        tool_args = tc.get("args", {})
                        logger.info("Tool call: %s, args: %s", tool_name, tool_args)
                        if tool_service and tool_name == "weather_query":
                            try:
                                tool_args.setdefault("query", req.message)
                                result_text = await tool_service.ainvoke(tool_args)
                                logger.info("Tool result: %s...", result_text[:200])
                                tool_messages.append(result_text)
                            except Exception:
                                logger.exception("Weather query failed")
                                tool_messages.append("天气查询服务暂不可用，请稍后重试。")
                        elif tool_service and tool_name == "tavily_search":
                            try:
                                raw_query = tool_args.get("query", req.message)
                                enhanced_query = f"{raw_query} {now.year}年{now.month}月{now.day}日 天气"
                                logger.info("Enhanced tavily query: %s", enhanced_query)
                                search_result = await tool_service.ainvoke({"query": enhanced_query})
                                result_text = WeatherToolService.format_search_results(search_result)
                                logger.info("Tool result: %s...", result_text[:200])
                                tool_messages.append(result_text)
                            except Exception:
                                logger.exception("Tavily search failed")
                                tool_messages.append("天气服务暂不可用，请稍后重试。")
                        elif alert_tool and tool_name == "alert_query":
                            try:
                                result = alert_tool.invoke(tool_args)
                                logger.info("Tool result: %s...", str(result)[:200])
                                tool_messages.append(result)
                            except Exception:
                                logger.exception("Alert query failed")
                                tool_messages.append("预警查询服务暂不可用，请稍后重试。")

                    final_prompt_parts = [
                        "你是一个专业的气象智能助手，帮助用户解答气象相关问题。",
                        "【重要指令】无论用户是否主动提及出行，你必须始终在回答的末尾或合适位置，基于当前的天气状况（如温度、降水、风力、空气质量、预警等）提供具体、实用的出行建议（例如穿衣、是否需要携带雨具、防晒防寒、户外运动适宜度等）。",
                        date_str,
                    ]
                    kb_ctx = KnowledgeBaseService.build_context(db, effective_knowledge_base_ids)
                    if kb_ctx:
                        final_prompt_parts.append("以下是相关气象知识库内容，请结合这些内容回答：\n" + kb_ctx)
                    if tool_messages:
                        final_prompt_parts.append("工具查询结果：\n" + "\n".join(tool_messages))
                    final_prompt_parts.append(
                        "请基于工具查询结果回答用户关于天气的具体情况。若工具结果包含多天数据，必须逐日列出；"
                        "若工具结果不足以回答完整天数，请说明数据不足，不要自行补全。"
                        "此外，你应当根据获得的天气信息自主生成对应的出行建议，这不受上述关于不能自行补全天气数据的限制。"
                    )

                    final_messages = [
                        SystemMessage(content="\n".join(final_prompt_parts)),
                        HumanMessage(content=req.message),
                    ]
                    filt = ThinkingFilter()
                    async for chunk in llm.astream(final_messages):
                        text = chunk.content if hasattr(chunk, "content") else ""
                        if text:
                            out = filt.feed(text)
                            if out:
                                assistant_content += out
                                yield SSEStream.event({"chunk": out})
                    rem = filt.flush()
                    if rem:
                        assistant_content += rem
                        yield SSEStream.event({"chunk": rem})
                else:
                    content = first_response.content if hasattr(first_response, "content") else ""
                    content = strip_thinking_tags(content)
                    if content:
                        assistant_content += content
                        yield SSEStream.event({"chunk": content})
            else:
                async for chunk in stream_llm_response(llm, lc_messages):
                    assistant_content += chunk
                    yield SSEStream.event({"chunk": chunk})

        except Exception as e:
            err_str = str(e)
            if config.get("is_local", False):
                if "502" in err_str or "Connection" in err_str or "Connect" in err_str:
                    error_msg = "本地模型未就绪，请确认 Ollama 已启动（默认端口 11434）。"
                elif "does not support tools" in err_str:
                    error_msg = "当前本地模型不支持工具调用，请切换为支持工具调用的模型，或取消勾选工具选项。"
                else:
                    error_msg = f"本地模型请求出错：{err_str}"
            else:
                error_msg = f"抱歉，服务暂时出现问题：{err_str}"
            assistant_content += error_msg
            yield SSEStream.event({"chunk": error_msg})

        finally:
            db_local = SessionLocal()
            try:
                ConversationService.add_message(db_local, conversation_id, "assistant", assistant_content)
            finally:
                db_local.close()
            yield SSEStream.event("[DONE]")

    return sse_response(event_generator())

# ---- 对话管理 ----
@router.get("/conversations", response_model=ConversationsResponse)
def list_conversations(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    items, total = ConversationService.list_by_user(db, current_user["user_id"], page, page_size)
    return ConversationsResponse(
        conversations=[
            ConversationItem(
                id=c.id,
                title=c.title,
                model_id=c.model_id,
                created_at=c.created_at,
                updated_at=c.updated_at,
            ) for c in items
        ],
        total=total,
    )

@router.post("/conversations", response_model=ConversationItem)
def create_conversation(
    req: CreateConversationRequest,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    conv = ConversationService.create(db, current_user["user_id"], req.title, req.model_id)
    return ConversationItem(
        id=conv.id,
        title=conv.title,
        model_id=conv.model_id,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
    )

@router.get("/conversations/{conversation_id}", response_model=ConversationDetail)
def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    conv = ConversationService.get(db, conversation_id, current_user["user_id"])
    if not conv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    messages = ConversationService.get_messages(db, conversation_id, current_user["user_id"])
    return ConversationDetail(
        id=conv.id,
        title=conv.title,
        model_id=conv.model_id,
        messages=[
            MessageItem(role=m.role, content=m.content, created_at=m.created_at)
            for m in messages
        ],
        created_at=conv.created_at,
        updated_at=conv.updated_at,
    )

@router.put("/conversations/{conversation_id}", response_model=ConversationItem)
def rename_conversation(
    conversation_id: str,
    req: RenameConversationRequest,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    conv = ConversationService.rename(db, conversation_id, current_user["user_id"], req.title)
    if not conv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    return ConversationItem(
        id=conv.id,
        title=conv.title,
        model_id=conv.model_id,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
    )

@router.post("/conversations/{conversation_id}/summarize")
def summarize_conversation(
    conversation_id: str,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    """使用 AI 自动总结并更新对话标题"""
    from app.services.conversation import ConversationService
    from app.services.llm import get_llm, strip_thinking_tags
    
    conv = ConversationService.get(db, conversation_id, current_user["user_id"])
    if not conv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
        
    first_msg = None
    for msg in conv.messages:
        if msg.role == "user":
            first_msg = msg.content
            break
            
    if not first_msg:
        return {"title": conv.title}
        
    try:
        # 使用会话的模型，参数偏向确定性（较小 temperature）
        llm = get_llm(conv.model_id, temperature=0.3, streaming=False, db=db)
        
        prompt = (
            "请根据以下用户的提问，总结生成一个非常简短、精准的中文对话标题（绝对不能超过6个字，直接输出标题文本，不要包含任何标点符号、引号、破折号、前缀、空格或解释说明）：\n"
            f"用户提问：{first_msg}"
        )
        
        resp = llm.invoke(prompt)
        ai_title = strip_thinking_tags(resp.content)
        
        # 去除非文字字符
        ai_title = ai_title.replace('"', '').replace('“', '').replace('”', '').replace('《', '').replace('》', '').strip()
        if len(ai_title) > 10:
            ai_title = ai_title[:10]
            
        if ai_title:
            ConversationService.rename(db, conversation_id, current_user["user_id"], ai_title)
            return {"title": ai_title}
    except Exception as e:
        # fallback: 截取前 10 个字符，同时防止包含 thinking tag
        clean_msg = strip_thinking_tags(first_msg)
        fallback_title = clean_msg[:10] + "..." if len(clean_msg) > 10 else clean_msg
        ConversationService.rename(db, conversation_id, current_user["user_id"], fallback_title)
        return {"title": fallback_title}
        
    return {"title": conv.title}

@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    ok = ConversationService.delete(db, conversation_id, current_user["user_id"])
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    return {"detail": "Deleted"}

@router.post("/conversations/batch-delete")
def batch_delete_conversations(
    req: BatchDeleteRequest,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    count = ConversationService.batch_delete(db, req.conversation_ids, current_user["user_id"])
    return {"detail": f"Deleted {count} conversations"}

@router.post("/weather-card", response_model=WeatherCardResponse)
def generate_weather_card(
    req: WeatherCardRequest,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    import json
    from zoneinfo import ZoneInfo

    from app.models.model_config import ModelConfig

    user_id = current_user["user_id"]
    city = req.city.strip()
    weather = WeatherToolService.fetch_realtime_weather(city)
    if not weather:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"未能获取到 {city} 的天气数据，请确认城市名称是否正确。",
        )

    now = datetime.now(ZoneInfo("Asia/Shanghai"))
    date_key = now.strftime("%Y-%m-%d")
    deterministic_tarot_id = select_tarot_card_id(
        f"user:{user_id}",
        date_key,
    )
    tarot_id = req.tarot_card_id or deterministic_tarot_id
    tarot = TAROT_CARD_META.get(tarot_id) or TAROT_CARD_META[deterministic_tarot_id]

    model_id = req.model_id
    if not model_id:
        models = db.query(ModelConfig).order_by(ModelConfig.created_at.asc()).all()
        model_id = select_preferred_weather_oracle_model_id(models)
        if not model_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="没有可用的模型配置，请先到系统设置中配置 LLM。",
            )

    prompt = build_weather_oracle_prompt(weather, date_key, tarot)

    fallback = {
        "fortune": {
            "title": "云隙微光",
            "summary": "今天适合先观察，再行动。把节奏放慢一点，很多事会自然变清楚。",
            "lucky_color": "雾紫色",
            "lucky_number": 7,
            "good_for": "整理思路",
            "avoid": "冲动争执",
        },
        "mood_guide": {
            "title": "缓慢回神",
            "analysis": "天气信号偏向内收，适合减少无效沟通，把精力留给真正需要处理的事。",
            "suggestions": ["留二十分钟独处", "喝点热饮", "把决定放到明天"],
        },
        "daily_advice": build_weather_daily_advice(weather),
        "weather_mappings": [
            {
                "metric": "temperature",
                "label": "温度",
                "value": format_weather_metric_value(weather.get("temperature"), "°C"),
                "reading": "平和舒适",
                "score": 70,
            },
            {
                "metric": "humidity",
                "label": "湿度",
                "value": format_weather_metric_value(weather.get("humidity"), "%"),
                "reading": "内收敏感",
                "score": 65,
            },
            {
                "metric": "pressure",
                "label": "气压",
                "value": format_weather_metric_value(weather.get("pressure"), " hPa"),
                "reading": "掌控感提升",
                "score": 68,
            },
            {
                "metric": "wind_speed",
                "label": "风速",
                "value": format_weather_metric_value(weather.get("wind_speed"), " km/h"),
                "reading": "思绪流动",
                "score": 60,
            },
        ],
    }

    response_payload = {
        "city": weather["city"],
        "date": date_key,
        "timezone": "Asia/Shanghai",
        "updated_at": now.isoformat(),
        "weather": weather,
        "tarot": tarot,
        "fortune": fallback["fortune"],
        "mood_guide": fallback["mood_guide"],
        "daily_advice": fallback["daily_advice"],
        "weather_mappings": fallback["weather_mappings"],
    }
    try:
        llm = get_llm(
            model_id,
            temperature=0.3,
            streaming=False,
            db=db,
            timeout=20.0,
            max_retries=0,
            use_env_proxy=False,
        )
        resp = llm.invoke(prompt)
        card_data = json.loads(clean_json_object_text(resp.content))
        normalized_card_data = normalize_weather_oracle_model_data(card_data, fallback)
        model_payload = {
            "city": weather["city"],
            "date": date_key,
            "timezone": "Asia/Shanghai",
            "updated_at": now.isoformat(),
            "weather": weather,
            "tarot": tarot,
            "fortune": normalized_card_data["fortune"],
            "mood_guide": normalized_card_data["mood_guide"],
            "daily_advice": normalized_card_data["daily_advice"],
            "weather_mappings": normalized_card_data["weather_mappings"],
        }
        return WeatherCardResponse.model_validate(model_payload, strict=True)
    except HTTPException:
        raise
    except Exception:
        logger.exception("Failed to generate weather oracle JSON; using fallback")

    return WeatherCardResponse.model_validate(response_payload, strict=True)
