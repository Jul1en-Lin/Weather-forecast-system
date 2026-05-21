from pydantic import BaseModel
from typing import Optional

class ConfigResponse(BaseModel):
    kimi_api_key: str
    deepseek_api_key: str
    minimax_api_key: str
    tavily_api_key: str
    qweather_api_key: str
    qweather_api_host: str
    ollama_base_url: str

class ConfigUpdate(BaseModel):
    kimi_api_key: Optional[str] = None
    deepseek_api_key: Optional[str] = None
    minimax_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None
    qweather_api_key: Optional[str] = None
    qweather_api_host: Optional[str] = None
    ollama_base_url: Optional[str] = None