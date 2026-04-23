import logging
from typing import Optional
import httpx
from langchain_tavily import TavilySearch
from langchain_core.tools import StructuredTool
from app.config import settings
from app.database import SessionLocal
from app.models.alert import Alert

logger = logging.getLogger(__name__)


def _query_alerts(alert_type: str = "", level: str = "") -> str:
    """Query meteorological alert definitions from database."""
    db = SessionLocal()
    try:
        q = db.query(Alert)
        if alert_type:
            q = q.filter(Alert.alert_type.contains(alert_type))
        if level:
            q = q.filter(Alert.level == level)
        alerts = q.limit(10).all()
        if not alerts:
            return "未查询到相关预警信号定义。"
        parts = []
        for a in alerts:
            parts.append(f"{a.alert_type}{a.level}预警: 标准={a.criteria}; 防御={a.response_guide or '无'}")
        return "\n".join(parts)
    finally:
        db.close()


def _fetch_realtime_alerts(location: str = "") -> str:
    """Fetch real-time weather alerts via QWeather API, fallback to DB definitions."""
    if not settings.qweather_api_key:
        logger.info("QWeather API key not configured, falling back to DB alert definitions")
        db_result = _query_alerts(alert_type=location)
        if "未查询到" in db_result:
            return "暂未查询到实时气象预警信息。（实时预警服务未配置，仅提供预警信号标准定义查询）"
        return f"【预警信号标准定义】\n{db_result}\n\n（以上为预警信号标准定义，非实时预警）"

    try:
        # QWeather uses location ID or lat/lon; here we try a geo lookup first
        # For simplicity, use the city-warning endpoint with location keyword
        host = settings.qweather_api_host
        geo_url = f"https://{host}/geo/v2/city/lookup"
        geo_params = {"location": location or "", "key": settings.qweather_api_key, "number": 1}
        with httpx.Client(timeout=10.0) as client:
            geo_resp = client.get(geo_url, params=geo_params)
            geo_data = geo_resp.json()
            location_id = ""
            if geo_data.get("code") == "200" and geo_data.get("location"):
                location_id = geo_data["location"][0].get("id", "")

            if location_id:
                warn_url = f"https://{host}/v7/warning/now"
                warn_params = {"location": location_id, "key": settings.qweather_api_key}
                warn_resp = client.get(warn_url, params=warn_params)
                warn_data = warn_resp.json()

                if warn_data.get("code") == "200":
                    warnings = warn_data.get("warning", [])
                    if not warnings:
                        return f"{location or '该地区'} 当前暂无生效的气象预警信号。"
                    parts = [f"【实时气象预警 — {location or '查询地区'}】"]
                    for w in warnings:
                        parts.append(
                            f"- {w.get('title', '未知预警')}（{w.get('pubTime', '时间未知')}）\n"
                            f"  类型：{w.get('typeName', '未知')} | 级别：{w.get('level', '未知')}\n"
                            f"  发布单位：{w.get('sender', '未知')}\n"
                            f"  防御建议：{w.get('text', '暂无详细防御建议')[:300]}"
                        )
                    return "\n".join(parts)

        # API call succeeded but no valid data
        logger.warning("QWeather API returned no valid warning data")
    except Exception as e:
        logger.exception("QWeather API call failed: %s", e)

    # Fallback to DB definitions
    db_result = _query_alerts(alert_type=location)
    if "未查询到" in db_result:
        return "预警查询服务暂不可用，未获取到实时预警信息。"
    return f"【预警信号标准定义】\n{db_result}\n\n（以上为预警信号标准定义，非实时预警）"


class WeatherToolService:
    @staticmethod
    def get_tool():
        if not settings.tavily_api_key:
            return None
        return TavilySearch(
            tavily_api_key=settings.tavily_api_key,
            max_results=3,
            search_depth="basic",
        )

    @staticmethod
    def get_alert_tool():
        return StructuredTool.from_function(
            name="alert_query",
            description="查询实时气象预警信号。参数：location（城市/地区名称，如北京、上海）、alert_type（可选，如暴雨、台风）。",
            func=_fetch_realtime_alerts,
        )

    @staticmethod
    def format_tool_result(result) -> str:
        """Format TavilySearch result for LLM prompt."""
        if hasattr(result, "content"):
            return str(result.content)
        return str(result)

    @staticmethod
    def format_search_results(result) -> str:
        """Parse TavilySearch result into structured text with time annotations."""
        raw = WeatherToolService.format_tool_result(result)
        # Try to parse as list of dicts (TavilySearch may return a list or an object)
        items = []
        if isinstance(result, list):
            items = result
        elif hasattr(result, "results"):
            items = result.results
        elif hasattr(result, "content"):
            # Already plain text, return as-is with a header
            return f"【天气搜索结果】\n{raw}"

        if not items:
            return f"【天气搜索结果】\n{raw}"

        parts = ["【天气搜索结果】"]
        for idx, item in enumerate(items[:3], start=1):
            if isinstance(item, dict):
                title = item.get("title", "无标题")
                url = item.get("url", "")
                content = item.get("content", "")
                published = item.get("published_date", "")
            else:
                title = getattr(item, "title", "无标题")
                url = getattr(item, "url", "")
                content = getattr(item, "content", "")
                published = getattr(item, "published_date", "")

            date_str = published if published else "时间未知"
            content_snippet = (content[:500] + "...") if len(str(content)) > 500 else content
            parts.append(
                f"{idx}. {title}（{date_str}）\n"
                f"   来源：{url}\n"
                f"   摘要：{content_snippet}"
            )

        return "\n\n".join(parts)
