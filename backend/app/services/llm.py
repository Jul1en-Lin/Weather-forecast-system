from typing import AsyncIterator
from langchain_openai import ChatOpenAI
from app.config import settings

MODEL_CONFIG = {
    "kimi-k2.5": {
        "model": "kimi-k2.5",
        "base_url": "https://api.moonshot.cn/v1",
        "api_key": settings.kimi_api_key,
        "temperature": 1.0,  # Kimi K2.5 只接受 temperature=1
    },
    "deepseek-reasoner": {
        "model": "deepseek-reasoner",
        "base_url": "https://api.deepseek.com/v1",
        "api_key": settings.deepseek_api_key,
    },
    "MiniMax-M2.5": {
        "model": "MiniMax-M2.5",
        "base_url": "https://api.minimax.chat/v1",
        "api_key": settings.minimax_api_key,
    },
    "deepseek-r1:14b": {
        "model": "deepseek-r1:14b",
        "base_url": settings.ollama_base_url,
        "api_key": "ollama",
        "is_local": True,
    },
}

def get_llm(model_id: str, temperature: float = 0.7, streaming: bool = True) -> ChatOpenAI:
    config = MODEL_CONFIG.get(model_id)
    if not config:
        raise ValueError(f"Unknown model_id: {model_id}")
    kwargs = dict(
        model=config["model"],
        base_url=config["base_url"],
        api_key=config["api_key"],
        streaming=streaming,
    )
    # 若模型配置中指定了 temperature，优先使用；否则用传入值
    kwargs["temperature"] = config.get("temperature", temperature)
    return ChatOpenAI(**kwargs)

async def stream_llm_response(llm: ChatOpenAI, messages: list) -> AsyncIterator[str]:
    """Yield text chunks from LLM stream."""
    async for chunk in llm.astream(messages):
        content = chunk.content if hasattr(chunk, "content") else ""
        if content:
            yield content
