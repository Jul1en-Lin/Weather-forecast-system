from pydantic_settings import BaseSettings
from typing import Optional
import threading

class Settings(BaseSettings):
    database_url: str = "sqlite:///./database.sqlite"
    kimi_api_key: str = ""
    deepseek_api_key: str = ""
    minimax_api_key: str = ""
    tavily_api_key: str = ""
    qweather_api_key: str = ""
    qweather_api_host: str = "devapi.qweather.com"
    ollama_base_url: str = "http://localhost:11434/v1"
    app_secret_key: str = "change-me"
    allowed_origins: str = "http://localhost:5173"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def update_config(self, **kwargs) -> None:
        """更新配置（线程安全）"""
        with _config_lock:
            for key, value in kwargs.items():
                if hasattr(self, key) and value is not None:
                    setattr(self, key, value)

    def get_config_dict(self, mask_secrets: bool = True) -> dict:
        """获取配置字典（可选掩码敏感信息）"""
        with _config_lock:
            config = {
                "kimi_api_key": self.kimi_api_key,
                "deepseek_api_key": self.deepseek_api_key,
                "minimax_api_key": self.minimax_api_key,
                "tavily_api_key": self.tavily_api_key,
                "qweather_api_key": self.qweather_api_key,
                "qweather_api_host": self.qweather_api_host,
                "ollama_base_url": self.ollama_base_url,
            }
        if mask_secrets:
            for key in config:
                if config[key]:
                    config[key] = mask_api_key(config[key])
        return config

def mask_api_key(key: str) -> str:
    """掩码 API Key，只显示前4位和后4位"""
    if len(key) <= 8:
        return "***"
    return key[:4] + "..." + key[-4:]

_config_lock = threading.Lock()
settings = Settings()
