from typing import Optional
from langchain_tavily import TavilySearch
from langchain_core.tools import StructuredTool
from app.config import settings
from app.database import SessionLocal
from app.models.alert import Alert


def _query_alerts(alert_type: str = "", level: str = "") -> str:
    """Query meteorological alert signals from database."""
    db = SessionLocal()
    try:
        q = db.query(Alert)
        if alert_type:
            q = q.filter(Alert.alert_type.contains(alert_type))
        if level:
            q = q.filter(Alert.level == level)
        alerts = q.limit(10).all()
        if not alerts:
            return "未查询到相关预警信号。"
        parts = []
        for a in alerts:
            parts.append(f"{a.alert_type}{a.level}预警: 标准={a.criteria}; 防御={a.response_guide or '无'}")
        return "\n".join(parts)
    finally:
        db.close()


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
            description="查询气象预警信号。可选参数：alert_type（预警类型，如台风、暴雨、高温）、level（预警级别：蓝、黄、橙、红）。",
            func=_query_alerts,
        )

    @staticmethod
    def format_tool_result(result) -> str:
        """Format TavilySearch result for LLM prompt."""
        if hasattr(result, "content"):
            return str(result.content)
        return str(result)
