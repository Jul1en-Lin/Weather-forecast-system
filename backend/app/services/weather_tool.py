from typing import Optional
from langchain_tavily import TavilySearch
from app.config import settings


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
    def format_tool_result(result) -> str:
        """Format TavilySearch result for LLM prompt."""
        if hasattr(result, "content"):
            return str(result.content)
        return str(result)
