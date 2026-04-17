from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    kimi_api_key: str = ""
    deepseek_api_key: str = ""
    minimax_api_key: str = ""
    tavily_api_key: str = ""
    ollama_base_url: str = "http://localhost:11434/v1"
    app_secret_key: str = "change-me"
    allowed_origins: str = "http://localhost:5173"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
