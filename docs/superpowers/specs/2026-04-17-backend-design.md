# 后端实现设计文档

> 基于 `docs/project_spec.md`，采用**方案二：按功能模块逐个冲刺**。

---

## 1. 设计概述

### 目标
构建 FastAPI 后端，为前端 Vue 3 SPA 提供 Session-Cookie 认证、对话管理、流式 SSE 对话（LangChain 编排）、知识库 SQL 注入、天气工具调用等完整能力。

### 实现顺序
1. 项目骨架（配置、数据库、目录结构）
2. 认证模块（Session-Cookie 登录/登出/Me）
3. 对话管理 CRUD（创建、列表、详情、重命名、删除）
4. 模型列表（`GET /models`）
5. 知识库与工具列表（`GET /knowledge-bases`、`GET /tools`）
6. 流式对话（SSE + LangChain + 多轮上下文 — 核心功能）
7. 知识库注入 + 天气工具调用（在流式对话中集成）

---

## 2. 目录结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 入口、生命周期、CORS、中间件
│   ├── config.py               # Pydantic Settings，读取 .env
│   ├── dependencies.py         # DB Session、当前用户获取
│   ├── database.py             # SQLAlchemy engine、session、表创建
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py         # bcrypt 哈希、session 签发与校验
│   │   └── sse.py              # SSE StreamingResponse 封装
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── conversation.py
│   │   ├── message.py
│   │   ├── term.py
│   │   └── alert.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── assistant.py
│   │   └── conversation.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── assistant.py
│   └── services/
│       ├── __init__.py
│       ├── llm.py              # ChatOpenAI 初始化、模型映射、流式调用
│       ├── knowledge_base.py   # 知识库 SQL 查询与 prompt 注入
│       ├── weather_tool.py     # TavilySearch 封装
│       └── conversation.py     # 对话 CRUD、上下文组装
├── .env
├── requirements.txt
└── README.md
```

---

## 3. 数据库设计

严格遵循 `project_spec.md` 2.3 节五张表：`users`、`conversations`、`messages`、`terms`、`alerts`。

建表策略：后端启动时 `Base.metadata.create_all()` 自动建表（开发阶段）。

---

## 4. 认证设计

### 机制
Session-Cookie，session 数据存储于内存（Python dict），session_id 通过 `Set-Cookie` 下发。

### 流程
- 登录：`POST /api/v1/auth/login` → 验证 bcrypt 密码 → 生成 session_id → 存入内存 + Set-Cookie
- 登出：`POST /api/v1/auth/logout` → 删除内存中的 session
- Me：`GET /api/v1/auth/me` → 从 Cookie 取 session_id → 查内存 → 返回用户信息
- 受保护接口依赖 `get_current_user`：无有效 session 返回 401

---

## 5. 流式对话设计（核心）

### 时序
```
Client → POST /chat/stream
       → FastAPI 查询历史 messages（若 conversation_id 存在）
       → SQL 查询知识库（若 knowledge_base_ids 非空）
       → 组装 LangChain messages（system + kb context + history + user）
       → ChatOpenAI.bind_tools(tools).astream()
       → SSE 逐 chunk 返回 data: {"chunk":"..."}
       → 最后 data: [DONE]
       → 保存 user message + assistant message 到 MySQL
```

### SSE 格式
```
data: {"chunk":"今天北京"}

data: {"chunk":"天气晴朗"}

data: [DONE]
```

### 工具调用策略
- 首轮：`bind_tools` → 获取 `tool_calls`
- 执行 TavilySearch
- 将结果回传模型生成最终回答
- 若 Moonshot 二次回传报 400，采用两阶段稳妥方案（本地执行工具后构造最终 prompt）

### 模型映射
| model_id | base_url | api_key env |
|---------|---------|------------|
| kimi-k2.5 | https://api.moonshot.cn/v1 | KIMI_API_KEY |
| deepseek-reasoner | https://api.deepseek.com/v1 | DEEPSEEK_API_KEY |
| MiniMax-M2.5 | https://api.minimax.chat/v1 | MINIMAX_API_KEY |
| deepseek-r1:14b | http://localhost:11434/v1 | 无 |

---

## 6. 知识库消费方式

**非 RAG，纯 SQL 查询后注入 prompt**：
- `terms` 表 → 按 term 名或 category 查询 → 拼入 system prompt
- `alerts` 表 → 按 alert_type 或 level 查询 → 拼入 system prompt

---

## 7. 错误处理与回退

| 场景 | 响应 |
|-----|------|
| Ollama 未启动 | 503，前端提示"本地模型未就绪" |
| Tavily 限流/失败 | 直接回复"天气服务暂不可用"，不中断对话 |
| Session 过期 | 401 |
| 模型 ID 不存在 | 400 |

---

## 8. 环境变量（.env）

```bash
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/meteo_assistant
KIMI_API_KEY=sk-xxxxxxxx
DEEPSEEK_API_KEY=sk-xxxxxxxx
MINIMAX_API_KEY=xxxxxxxx
TAVILY_API_KEY=tvly-xxxxxxxx
OLLAMA_BASE_URL=http://localhost:11434/v1
APP_SECRET_KEY=your-secret-key-change-in-production
ALLOWED_ORIGINS=http://localhost:5173
```

---

## 9. 前端适配点

后端完成后，前端需做以下适配：
1. `auth.ts`：login/logout 调用真实 API，不再用 localStorage 存认证态
2. `IntelligentAssistant.vue`：流式响应从 `mockStreamReply` 改为调用 `/chat/stream` SSE
3. 对话数据从 `localStorage` 迁移到后端 API
4. 模型选项从硬编码改为调用 `/models` 动态获取

---

## 附录：变更记录

| 日期 | 变更内容 | 作者 |
|------|---------|------|
| 2026-04-17 | 后端实现设计文档，确认方案二（按模块逐个冲刺） | Claude |
