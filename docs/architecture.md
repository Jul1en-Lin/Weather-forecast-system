# 系统架构文档 (System Architecture)

## 架构图 (Architecture Diagram)

<!-- 在此插入系统架构图 -->
```
[架构图占位区域]
```

## 核心组件说明 (Core Components)

<!-- 描述系统的核心组件及其职责 -->

| 组件名称 | 职责描述 | 关键文件/模块 |
|---------|---------|--------------|
| 前端 SPA | 用户界面，智能助手对话 | Vue 3 + Vite + TypeScript |
| API 网关 | RESTful API + SSE 流式服务 | FastAPI (`backend/app/main.py`) |
| 认证模块 | Session-Cookie 登录态管理 | `backend/app/core/security.py`, `backend/app/routers/auth.py` |
| 用户管理 | 用户注册、权限管理 | `backend/app/routers/users.py`, `backend/app/models/user.py` |
| 配置管理 | 运行时配置更新 | `backend/app/routers/config.py`, `backend/app/config.py` |
| 对话服务 | 对话 CRUD、消息管理 | `backend/app/services/conversation.py` |
| LLM 服务 | 模型初始化、流式调用 | `backend/app/services/llm.py` |
| 知识库服务 | SQL 查询后注入 prompt | `backend/app/services/knowledge_base.py` |
| 天气工具 | TavilySearch 封装 | `backend/app/services/weather_tool.py` |
| 数据层 | SQLite ORM | `backend/app/models/*.py`, `backend/app/database.py` |

## 技术栈清单 (Tech Stack)

### 前端
| 类别 | 技术选型 | 版本 | 用途说明 |
|-----|---------|-----|---------|
| 框架 | Vue 3 | 3.x | SPA 框架 |
| 构建 | Vite | — | 构建工具 |
| 语言 | TypeScript | — | 类型安全 |
| 路由 | Vue Router | — | 前端路由 |
| 状态 | Pinia | — | 状态管理 |

### 后端
| 类别 | 技术选型 | 版本 | 用途说明 |
|-----|---------|-----|---------|
| 语言 | Python | >=3.10 | 后端主语言 |
| 框架 | FastAPI | >=0.110 | Web 框架 |
| 服务器 | Uvicorn | >=0.27 | ASGI 服务器 |
| ORM | SQLAlchemy | >=2.0 | SQLite 数据访问 |
| 驱动 | Python sqlite3 | — | SQLite 内置驱动（无外部依赖） |
| LLM 编排 | LangChain | >=0.1 | 模型调用、工具绑定 |
| LLM SDK | langchain-openai | >=0.1 | 兼容 OpenAI 风格 API |
| 搜索工具 | langchain-tavily | >=0.1 | 天气搜索 |
| 密码哈希 | bcrypt | — | 用户密码存储 |
| Session | 内存 dict | — | 开发阶段认证 |

## 架构决策记录 (Architecture Decision Records)

| 日期 | 决策内容 | 原因/背景 |
|-----|---------|----------|
| 2026-04-17 | 后端采用 FastAPI + SQLAlchemy + LangChain | 团队技术栈统一，async 原生支持 SSE |
| 2026-04-17 | Session 存储于内存（非 Redis/MySQL） | 当前阶段可接受，后续如需持久化再迁移 |
| 2026-04-17 | 知识库采用 SQL 注入 prompt（非 RAG） | 数据量小，SQL 查询更简单可控 |
| 2026-04-17 | 工具调用采用两阶段稳妥方案 | Moonshot 二次回传可能报 400，规避兼容性问题 |
| 2026-05-09 | 数据库从 MySQL 迁移到 SQLite | 开发环境无需安装 MySQL 服务，开箱即用；SQLAlchemy 自动适配 Dialect，生产环境可按需切换回 MySQL |
| 2026-05-09 | `npm run dev` 一键启动前后端 | 使用 `concurrently` 同时启动 Vite 前端和 Uvicorn 后端，简化开发流程 |
