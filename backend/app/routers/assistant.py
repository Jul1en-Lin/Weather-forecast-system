from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from app.dependencies import get_db_session, get_current_user
from app.services.conversation import ConversationService
from app.services.llm import get_llm, stream_llm_response
from app.services.knowledge_base import KnowledgeBaseService
from app.services.weather_tool import WeatherToolService
from app.core.sse import sse_response, SSEStream
from app.database import SessionLocal
from app.schemas.assistant import (
    ModelsResponse, ModelInfo,
    KnowledgeBasesResponse, KnowledgeBaseInfo,
    ToolsResponse, ToolInfo,
    ChatStreamRequest,
    SpeechToTextResponse,
)
from app.schemas.conversation import (
    ConversationsResponse, ConversationItem,
    ConversationDetail, MessageItem,
    CreateConversationRequest, RenameConversationRequest,
    BatchDeleteRequest,
)

router = APIRouter(prefix="/api/v1/assistant", tags=["assistant"])

# ---- 模型列表 ----
@router.get("/models", response_model=ModelsResponse)
def get_models():
    return ModelsResponse(models=[
        ModelInfo(id="kimi-k2.5", name="Kimi K2.5", description="Moonshot 高性能模型"),
        ModelInfo(id="MiniMax-M2.5", name="MiniMax M2.5", description="MiniMax 通用模型"),
        ModelInfo(id="deepseek-reasoner", name="DeepSeek Reasoner", description="DeepSeek 推理模型"),
        ModelInfo(id="deepseek-r1:14b", name="DeepSeek R1 14B (本地)", description="Ollama 本地模型"),
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
    else:
        conv = ConversationService.create(db, user_id, req.message[:30], req.model_id)

    conversation_id = conv.id
    ConversationService.add_message(db, conversation_id, "user", req.message)
    history_msgs = ConversationService.get_messages(db, conversation_id, user_id)

    system_parts = ["你是一个专业的气象智能助手，帮助用户解答气象相关问题。"]
    kb_context = KnowledgeBaseService.build_context(db, req.knowledge_base_ids)
    if kb_context:
        system_parts.append("以下是相关气象知识库内容，请结合这些内容回答：\n" + kb_context)

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
    if req.tool_ids:
        if "weather_query" in req.tool_ids:
            tool_service = WeatherToolService.get_tool()
            if tool_service:
                tools.append(tool_service)
        if "alert_query" in req.tool_ids:
            alert_tool = WeatherToolService.get_alert_tool()
            if alert_tool:
                tools.append(alert_tool)

    async def event_generator():
        assistant_content = ""
        try:
            llm = get_llm(req.model_id, streaming=True)
            if tools:
                bound_llm = llm.bind_tools(tools)
                first_response = await bound_llm.ainvoke(lc_messages)
                tool_calls = first_response.tool_calls if hasattr(first_response, "tool_calls") else []

                if tool_calls:
                    tool_messages = []
                    for tc in tool_calls:
                        tool_name = tc.get("name", "")
                        tool_args = tc.get("args", {})
                        if tool_service and tool_name == "tavily_search":
                            try:
                                query = tool_args.get("query", req.message)
                                search_result = await tool_service.ainvoke({"query": query})
                                result_text = WeatherToolService.format_tool_result(search_result)
                                tool_messages.append(result_text)
                            except Exception:
                                tool_messages.append("天气服务暂不可用，请稍后重试。")
                        elif alert_tool and tool_name == "alert_query":
                            try:
                                result = alert_tool.invoke(tool_args)
                                tool_messages.append(result)
                            except Exception:
                                tool_messages.append("预警查询服务暂不可用，请稍后重试。")

                    final_prompt_parts = ["\n".join(system_parts)]
                    if tool_messages:
                        final_prompt_parts.append("工具查询结果：\n" + "\n".join(tool_messages))
                    final_prompt_parts.append("请根据以上信息回答用户。")

                    final_messages = [
                        SystemMessage(content="\n".join(final_prompt_parts)),
                        HumanMessage(content=req.message),
                    ]
                    async for chunk in llm.astream(final_messages):
                        text = chunk.content if hasattr(chunk, "content") else ""
                        if text:
                            assistant_content += text
                            yield SSEStream.event({"chunk": text})
                else:
                    content = first_response.content if hasattr(first_response, "content") else ""
                    if content:
                        assistant_content += content
                        yield SSEStream.event({"chunk": content})
            else:
                async for chunk in stream_llm_response(llm, lc_messages):
                    assistant_content += chunk
                    yield SSEStream.event({"chunk": chunk})

        except Exception as e:
            err_str = str(e)
            if req.model_id == "deepseek-r1:14b" and ("502" in err_str or "Connection" in err_str or "Connect" in err_str):
                error_msg = "本地模型未就绪，请确认 Ollama 已启动（默认端口 11434）。"
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

# ---- 语音转文字（预留） ----
@router.post("/speech-to-text", response_model=SpeechToTextResponse)
def speech_to_text():
    return SpeechToTextResponse(text="")
