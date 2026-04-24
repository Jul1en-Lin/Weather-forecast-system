import re
from typing import AsyncIterator
from langchain_openai import ChatOpenAI
from app.config import settings

MODEL_CONFIG = {
    "kimi-k2.5": {
        "model": "kimi-k2.5",
        "base_url": "https://api.moonshot.cn/v1",
        "api_key": settings.kimi_api_key,
        "temperature": 1.0,
        "supports_tools": True,
    },
    "deepseek-reasoner": {
        "model": "deepseek-reasoner",
        "base_url": "https://api.deepseek.com/v1",
        "api_key": settings.deepseek_api_key,
        "supports_tools": True,
    },
    "MiniMax-M2.5": {
        "model": "MiniMax-M2.5",
        "base_url": "https://api.minimax.chat/v1",
        "api_key": settings.minimax_api_key,
        "supports_tools": True,
    },
    "deepseek-r1:14b": {
        "model": "deepseek-r1:14b",
        "base_url": settings.ollama_base_url,
        "api_key": "ollama",
        "is_local": True,
        "supports_tools": False,
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

def strip_thinking_tags(text: str) -> str:
    """去除 <think>...</think> 标签及其内容（非流式使用）。"""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)


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
