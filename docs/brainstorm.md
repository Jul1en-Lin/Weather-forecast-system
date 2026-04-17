我是一个后端开发人员，现在这个项目轮到我接手实现后端服务了
要求：

技术栈：
python langchain
数据存储：对话记录、气象术语库、预警信号库，使用 MySQL 存储
LLM：实现流式传输
Web：选择FastAPI，后端代码目录结构根据后端标准开发组织。已有的结构目录不管是否合乎标准暂时搁置，后续考虑重新组织整理

LLM 调用方式：
1. API：统一使用 langchain-openai SDK配置，使用 Deepseek、minimax、kimi
2. 本地 Ollama：已有deepseek-r1:14b，默认端口

气象服务：
使用 langchain_tavily TavilySearch 

示例代码：
---
# 定义模型
import json
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

model = ChatOpenAI(
    model="kimi-k2.5",
    base_url="https://api.moonshot.cn/v1",
    reasoning_effort=None,
    timeout=30,
    max_retries=1,
)

# 定义工具
tool = TavilySearch(max_results=4)

# 绑定工具
model_with_tools = model.bind_tools(tools=[tool], tool_choice="auto")

# 定义消息列表
messages = [
    HumanMessage("北京今天的天气怎么样？")
]
ai_message = model_with_tools.invoke(messages)
search_results = []
for tool_call in ai_message.tool_calls:
    # TavilySearch 需要传入 tool_call 中的 args
    tool_result = tool.invoke(tool_call["args"])
    search_results.append(tool_result)

if ai_message.tool_calls:
    # Moonshot 在工具二次回传链路上可能报 400，这里改为两阶段稳妥方案
    final_prompt = (
        "你是一名天气助手。请根据以下 Tavily 检索结果回答用户问题，"
        "先给结论，再给 3 条出行建议。\n\n"
        f"用户问题: {messages[0].content}\n\n"
        f"检索结果(JSON): {json.dumps(search_results, ensure_ascii=False)}"
    )
    final = model.invoke([HumanMessage(final_prompt)])
    print(final.content)
else:
    # 没有触发工具时直接输出首轮回答，避免额外等待
    print(ai_message.content)
---

语音转文字服务：暂时不实现

补充说明：
登录验证：后端采用最简单的Session-Cookie方案即可。登录时需要对接真实用户数据库。 
前端已有的deepseek-32b改为Deepseek最新的支持API的模型（deepseek-reasoner）。
前端期望格式是SSE-chunk，后端需要维护多轮对话上下文，将历史信息传给langchain。 