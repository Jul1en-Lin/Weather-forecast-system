# 项目规格文档 (Project Specification)

> 本文档整合 `docs/brainstorm.md` 与边界问题澄清结果，作为前后端开发的唯一规格源。
> **规则**：若代码实现与本文档不符，以本文档为准；若需修改规格，必须先获得确认。

---

## 第一部分：PRD（产品需求文档）

### 1.1 产品概述

大语言模型气象业务应用平台后端服务，为前端 Vue 3 SPA 提供 RESTful API 与 SSE 流式对话能力，支撑智能气象问答、多轮对话上下文管理、知识库检索、天气工具调用及用户认证。

### 1.2 功能需求

#### FR-001 用户认证
- 提供基于 **Session-Cookie** 的登录与登出接口。
- 登录时验证用户名与密码，对接 MySQL 用户表。
- Session 数据存储于**内存**中。
- 未认证用户访问受保护接口时返回 `401 Unauthorized`。

#### FR-002 智能助手流式对话
- 端点：`POST /api/v1/assistant/chat/stream`
- 请求体字段：`model_id`、`message`、`conversation_id`（可选）、`knowledge_base_ids`（可选）、`tool_ids`（可选）
- 返回：`text/event-stream`（SSE），逐字/逐段推送大模型生成内容。
- 后端需维护多轮对话上下文：若提供 `conversation_id`，从 MySQL 查询历史消息并注入 LangChain 消息链；否则创建新对话。
- 前端模型映射以后端为准：前端 `deepseek-32b` 等选项为 mock，实际可用模型由 `/api/v1/assistant/models` 返回。

#### FR-003 模型管理
- 端点：`GET /api/v1/assistant/models`
- 返回当前后端支持的模型列表，包含 `id`、`name`、`description`。
- 支持的模型：
  - `kimi-k2.5`（Moonshot）
  - `MiniMax-M2.5`
  - `deepseek-reasoner`（DeepSeek）
  - `deepseek-r1:14b`（本地 Ollama）
- 各模型通过 `langchain-openai` SDK 配置，使用官方提供的 `base_url` 与 `api_key`。

#### FR-004 知识库（气象术语库 / 预警信号库）
- 端点：`GET /api/v1/assistant/knowledge-bases`
- 知识库存储于 MySQL，后端自行设计 Schema。
- 消费方式：**SQL 查询后将结果文本注入 prompt**，而非 RAG/向量检索。
- 当用户勾选知识库后，后端在构造 prompt 时先查询对应 MySQL 表，将结果作为上下文一并传给 LLM。

#### FR-005 工具调用（天气查询 / 预警查询）
- 端点：`GET /api/v1/assistant/tools`
- **天气查询**：使用 `langchain_tavily.TavilySearch`。工具调用流程遵循 LangChain 标准：模型 `bind_tools` → 判断调用 → 执行工具 → 二次回传结果生成最终回答。若 Moonshot 在二次回传链路报 `400`，采用两阶段稳妥方案（参考 brainstorm 示例代码）。
- **时间上下文注入**：构造 system prompt 时，必须动态注入当前日期（格式：`今天是 YYYY年M月D日，星期X。`），使模型明确知道查询基准日。
- **查询词增强**：调用 TavilySearch 时，将 LLM 生成的原始查询词强制拼接当前日期与地点关键词（格式：`{原始查询} YYYY年M月D日 天气`），提高搜索精准度。
- **预警查询**：`alert_query` 工具优先调用 QWeather 实时预警 API；若未配置 API Key 或调用失败，fallback 到数据库中的预警信号定义，并附注"（以上为预警信号标准定义，非实时预警）"。
- **搜索结果后处理**：TavilySearch 原始返回内容需解析为结构化文本，标注每条结果的标题、来源 URL、发布时间（若可用）及内容摘要（≤500 字符），以【天气搜索结果】标题输出。

#### FR-006 对话管理
- 端点：
  - `GET /api/v1/assistant/conversations` — 分页获取对话列表
  - `POST /api/v1/assistant/conversations` — 创建新对话
  - `GET /api/v1/assistant/conversations/{id}` — 获取对话详情（含消息列表）
  - `PUT /api/v1/assistant/conversations/{id}` — 重命名对话
  - `DELETE /api/v1/assistant/conversations/{id}` — 删除对话
  - `POST /api/v1/assistant/conversations/batch-delete` — 批量删除
- 对话及消息持久化到 MySQL。

#### FR-007 语音转文字
- 端点：`POST /api/v1/assistant/speech-to-text`
- **暂不实现**，接口预留，逻辑以前端为准。

---

## 第二部分：EDD（工程设计文档）

### 2.1 技术栈

| 类别 | 技术选型 | 版本约束 | 用途说明 |
|------|---------|---------|---------|
| 编程语言 | Python | >= 3.10 | 后端主语言 |
| Web 框架 | FastAPI | >= 0.110 | HTTP API / SSE 服务 |
| ASGI 服务器 | Uvicorn | >= 0.27 | 运行 FastAPI 应用 |
| LLM 编排 | LangChain | >= 0.1 | 模型调用、工具绑定、消息链管理 |
| LLM SDK | langchain-openai | >= 0.1 | 统一兼容 OpenAI 风格 API 的多厂商模型 |
| 天气搜索 | langchain-tavily | >= 0.1 | TavilySearch 工具 |
| 数据库 ORM | SQLAlchemy | >= 2.0 | MySQL 数据访问 |
| 数据库驱动 | PyMySQL 或 mysqlclient | — | MySQL 连接 |
| 密码哈希 | bcrypt | — | 用户密码存储 |
| Session 管理 | starlette-session 或自研内存中间件 | — | Session-Cookie 认证 |

### 2.2 目录结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 应用入口、生命周期、中间件
│   ├── config.py               # 配置管理（Pydantic Settings，读取 .env）
│   ├── dependencies.py         # 公共依赖：DB Session、当前用户、权限校验
│   ├── models/                 # SQLAlchemy ORM 模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── conversation.py
│   │   ├── message.py
│   │   ├── term.py             # 气象术语库
│   │   └── alert.py            # 预警信号库
│   ├── schemas/                # Pydantic 序列化 / 校验模型
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── assistant.py
│   │   └── conversation.py
│   ├── routers/                # API 路由
│   │   ├── __init__.py
│   │   ├── auth.py             # /login, /logout
│   │   └── assistant.py        # /api/v1/assistant/*
│   ├── services/               # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── llm.py              # LLM 初始化、模型映射、流式调用
│   │   ├── knowledge_base.py   # 知识库 SQL 查询与 prompt 注入
│   │   ├── weather_tool.py     # TavilySearch 工具封装
│   │   └── conversation.py     # 对话 CRUD、上下文组装
│   ├── core/                   # 核心工具
│   │   ├── __init__.py
│   │   ├── security.py         # 密码哈希、session 签发与校验
│   │   └── sse.py              # SSE 响应封装工具
│   └── database.py             # SQLAlchemy engine、session、表初始化
├── .env                        # 环境变量（不提交到 git）
├── requirements.txt            # Python 依赖
└── README.md                   # 后端启动说明
```

### 2.3 数据库设计（MySQL）

#### 2.3.1 users（用户表）
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,   -- bcrypt
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### 2.3.2 conversations（对话表）
```sql
CREATE TABLE conversations (
    id VARCHAR(36) PRIMARY KEY,            -- UUID
    user_id INT NOT NULL,
    title VARCHAR(200) DEFAULT '新对话',
    model_id VARCHAR(64) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

#### 2.3.3 messages（消息表）
```sql
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conversation_id VARCHAR(36) NOT NULL,
    role ENUM('user', 'assistant', 'system', 'tool') NOT NULL,
    content TEXT NOT NULL,
    tool_calls JSON DEFAULT NULL,          -- LangChain tool_calls JSON
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);
```

#### 2.3.4 terms（气象术语库）
```sql
CREATE TABLE terms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    term VARCHAR(100) NOT NULL,            -- 术语名
    category VARCHAR(50),                  -- 分类：如天气现象、预报用语
    definition TEXT NOT NULL,              -- 释义
    source VARCHAR(200),                   -- 来源标准/文献
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### 2.3.5 alerts（预警信号库）
```sql
CREATE TABLE alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alert_type VARCHAR(50) NOT NULL,       -- 预警类型：台风、暴雨、高温…
    level ENUM('蓝','黄','橙','红') NOT NULL,
    criteria TEXT NOT NULL,                -- 发布标准
    response_guide TEXT,                   -- 防御指南
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 2.4 模型配置（langchain-openai）

| 模型 ID | 提供商 | model 参数 | base_url | 备注 |
|---------|--------|-----------|----------|------|
| `kimi-k2.5` | Moonshot | `kimi-k2.5` | `https://api.moonshot.cn/v1` | 用户已确认 |
| `deepseek-reasoner` | DeepSeek | `deepseek-reasoner` | `https://api.deepseek.com/v1` | 官网文档 |
| `MiniMax-M2.5` | MiniMax | `MiniMax-M2.5` | `https://api.minimax.chat/v1` | 官网文档 |
| `deepseek-r1:14b` | Ollama（本地） | `deepseek-r1:14b` | `http://localhost:11434/v1` | 默认端口 |

> 各 API Key 通过 `.env` 注入，如 `KIMI_API_KEY`、`DEEPSEEK_API_KEY`、`MINIMAX_API_KEY`、`TAVILY_API_KEY`。Ollama 无需 API Key。

### 2.5 流式对话时序

```
Client                           FastAPI Backend                              MySQL
  |                                    |                                       |
  |-- POST /chat/stream -------------->|                                       |
  |   {model_id, message,              |                                       |
  |    conversation_id?,               |                                       |
  |    knowledge_base_ids?,            |                                       |
  |    tool_ids?}                      |                                       |
  |                                    |-- [若 conversation_id 存在]            |
  |                                    |   查询历史 messages ----------------->|
  |                                    |<-- 返回历史消息 -----------------------|
  |                                    |                                       |
  |                                    |-- [若 knowledge_base_ids 非空]         |
  |                                    |   SQL 查询 terms/alerts               |
  |                                    |                                       |
  |                                    |-- 组装 LangChain messages             |
  |                                    |   (system + kb context + history      |
  |                                    |    + user message)                    |
  |                                    |                                       |
  |                                    |-- ChatOpenAI.bind_tools(tools)        |
  |                                    |   .astream() 或 .ainvoke()            |
  |                                    |                                       |
  |<-- SSE: data: {"chunk":"..."} -----|   逐 chunk 输出                       |
  |<-- SSE: data: {"chunk":"..."} -----|                                       |
  |<-- SSE: data: [DONE] --------------|   流结束                              |
  |                                    |                                       |
  |                                    |-- 保存 user message + assistant        |
  |                                    |   message 到 messages 表 ------------>|
```

### 2.6 SSE 格式规范

```
HTTP/1.1 200 OK
Content-Type: text/event-stream; charset=utf-8
Cache-Control: no-cache
Connection: keep-alive

data: {"chunk":"今天北京"}

data: {"chunk":"天气晴朗"}

data: [DONE]

```

### 2.7 关键接口补充

以下接口未在 `openapi.yaml` 中定义，但为完整功能必须新增：

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `/api/v1/auth/login` | body: `{username, password}`；成功返回 `Set-Cookie: session_id=...` |
| `POST` | `/api/v1/auth/logout` | 清除 session cookie |
| `GET` | `/api/v1/auth/me` | 返回当前登录用户信息（可选，供前端初始化） |

### 2.8 配置项（.env 模板）

```bash
# 数据库
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/meteo_assistant

# API Keys
KIMI_API_KEY=sk-xxxxxxxx
DEEPSEEK_API_KEY=sk-xxxxxxxx
MINIMAX_API_KEY=xxxxxxxx
TAVILY_API_KEY=tvly-xxxxxxxx
QWEATHER_API_KEY=xxxxxxxx  # 和风天气实时预警 API（可选，未配置时 fallback 到 DB 定义）

# Ollama（本地，一般无需 key）
OLLAMA_BASE_URL=http://localhost:11434/v1

# 应用
APP_SECRET_KEY=your-secret-key-change-in-production
ALLOWED_ORIGINS=http://localhost:5173
```

### 2.9 风险与回退策略

| 风险 | 影响 | 回退策略 |
|------|------|---------|
| Moonshot 工具二次回传报 400 | 工具调用失败 | 采用两阶段稳妥方案：首轮获取 tool_calls → 本地执行工具 → 构造最终 prompt 二次调用模型 |
| Ollama 未启动或端口不通 | 本地模型不可用 | 返回 503，前端提示"本地模型未就绪" |
| Tavily API 限流/失败 | 天气查询无结果 | 直接回复用户"天气服务暂不可用"，不影响对话流 |
| Session 内存存储重启丢失 | 登录态失效 | 当前阶段可接受；后续如需持久化可迁移至 Redis/MySQL |

---

## 附录：变更记录

| 日期 | 变更内容 | 作者 |
|------|---------|------|
| 2026-04-17 | 初版 PRD + EDD，整合 brainstorm.md 与边界问题澄清结果 | Claude |
