import re
from typing import AsyncIterator
from langchain_openai import ChatOpenAI
from app.config import settings

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.model_config import ModelConfig
from app.services.httpx_compat import httpx_compatible_proxy_env

def get_model_config(model_id: str, db: Session = None) -> dict:
    """Build a fresh model config from the database and current runtime settings."""
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True
    try:
        try:
            model_cfg = db.query(ModelConfig).filter(ModelConfig.id == model_id).first()
        except Exception:
            model_cfg = None

        if model_cfg:
            config = {
                "model": model_cfg.model,
                "base_url": model_cfg.base_url,
                "api_key": model_cfg.api_key,
                "temperature": model_cfg.temperature,
                "supports_tools": model_cfg.supports_tools,
                "is_local": model_cfg.is_local,
            }
        else:
            # Fallback to defaults (useful for tests or during migration)
            defaults = {
                "kimi-k2.5": {
                    "model": "kimi-k2.5",
                    "base_url": "https://api.moonshot.cn/v1",
                    "temperature": 1.0,
                    "supports_tools": True,
                    "is_local": False
                },
                "deepseek-v4-flash": {
                    "model": "deepseek-v4-flash",
                    "base_url": "https://api.deepseek.com/v1",
                    "temperature": None,
                    "supports_tools": True,
                    "is_local": False
                },
                "MiniMax-M2.5": {
                    "model": "MiniMax-M2.5",
                    "base_url": "https://api.minimax.chat/v1",
                    "temperature": None,
                    "supports_tools": True,
                    "is_local": False
                },
                "deepseek-r1:14b": {
                    "model": "deepseek-r1:14b",
                    "base_url": None,
                    "temperature": None,
                    "supports_tools": False,
                    "is_local": True
                }
            }
            if model_id not in defaults:
                raise ValueError(f"Unknown model_id: {model_id}")
            config = dict(defaults[model_id])
            config["api_key"] = ""
        
        # Fallback to runtime settings if database/default value API key is empty
        if not config["api_key"]:
            if model_id == "kimi-k2.5" or config.get("model") == "kimi-k2.5":
                config["api_key"] = settings.kimi_api_key
            elif model_id == "deepseek-v4-flash" or config.get("model") == "deepseek-v4-flash":
                config["api_key"] = settings.deepseek_api_key
            elif model_id == "MiniMax-M2.5" or config.get("model") == "MiniMax-M2.5":
                config["api_key"] = settings.minimax_api_key
        
        if config["is_local"]:
            if not config["base_url"]:
                config["base_url"] = settings.ollama_base_url
            if not config["api_key"]:
                config["api_key"] = "ollama"
                
        return config
    finally:
        if close_db:
            db.close()


def get_llm(
    model_id: str,
    temperature: float = 0.7,
    streaming: bool = True,
    db: Session = None,
    timeout=None,
    max_retries=None,
) -> ChatOpenAI:
    config = get_model_config(model_id, db=db)
    kwargs = dict(
        model=config["model"],
        base_url=config["base_url"],
        api_key=config["api_key"],
        streaming=streaming,
    )
    # 若模型配置中指定了 temperature，优先使用；否则用传入值
    kwargs["temperature"] = config.get("temperature") if config.get("temperature") is not None else temperature
    if timeout is not None:
        kwargs["timeout"] = timeout
    if max_retries is not None:
        kwargs["max_retries"] = max_retries
    with httpx_compatible_proxy_env():
        return ChatOpenAI(**kwargs)

def strip_thinking_tags(text: str) -> str:
    """去除 <think>...</think> 标签及其内容（非流式使用），支持过滤未闭合的思维链。"""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    if "<think>" in text:
        text = text.split("<think>")[0]
    return text.strip()


class ThinkingFilter:
    """流式过滤 <think>...</think> 标签，处理跨 chunk 情况。"""

    def __init__(self):
        self.in_think = False
        self.buf = ""

    def feed(self, text: str) -> str:
        self.buf += text
        output = []

        while self.buf:
            if self.in_think:
                end = self.buf.find("</think>")
                if end == -1:
                    self.buf = self.buf[-10:] if len(self.buf) > 10 else self.buf
                    break
                self.buf = self.buf[end + len("</think>") :]
                self.in_think = False
            else:
                start = self.buf.find("<think>")
                if start == -1:
                    output.append(self.buf)
                    self.buf = ""
                    break
                output.append(self.buf[:start])
                self.buf = self.buf[start + len("<think>") :]
                self.in_think = True

        return "".join(output)

    def flush(self) -> str:
        text = self.buf
        self.buf = ""
        if self.in_think:
            return ""
        return text


async def filter_thinking_stream(iterator: AsyncIterator[str]) -> AsyncIterator[str]:
    filt = ThinkingFilter()
    async for chunk in iterator:
        out = filt.feed(chunk)
        if out:
            yield out
    out = filt.flush()
    if out:
        yield out


async def stream_llm_response(llm: ChatOpenAI, messages: list) -> AsyncIterator[str]:
    """Yield text chunks from LLM stream, filtering out thinking tags."""
    filt = ThinkingFilter()
    async for chunk in llm.astream(messages):
        content = chunk.content if hasattr(chunk, "content") else ""
        if content:
            out = filt.feed(content)
            if out:
                yield out
    out = filt.flush()
    if out:
        yield out
