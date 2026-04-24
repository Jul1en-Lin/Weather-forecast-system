# 大语言模型气象业务应用平台 — 项目汇报文档

## 一、项目概述

本项目是一款面向气象业务的大语言模型智能应用平台，采用前后端分离架构。前端为基于 Vue 3 的单页应用，提供智能气象问答对话界面；后端基于 FastAPI 构建，支持多模型流式对话、知识库检索、天气工具调用及用户认证。

### 核心功能

| 模块 | 功能描述 |
|------|----------|
| 智能对话 | 支持多轮对话上下文，SSE 流式输出，4 个模型可选 |
| 知识库 | 气象术语库、预警信号库，以 SQL 查询注入 Prompt 的方式增强回答 |
| 工具调用 | 天气实时查询（Tavily 搜索）、气象预警查询（QWeather API） |
| 对话管理 | 创建、切换、重命名、删除对话，历史消息持久化 |
| 用户认证 | Session-Cookie 登录认证 |

---

## 二、技术栈

| 层级 | 技术选型 | 版本/说明 |
|------|----------|-----------|
| **前端** | Vue 3 + Vite + TypeScript | Composition API，严格模式 |
| 状态管理 | Pinia | 持久化到 localStorage |
| 路由 | Vue Router | history 模式 |
| 样式 | 原生 CSS | Apple 风格设计令牌 |
| **后端** | FastAPI + Uvicorn | Python >= 3.10 |
| ORM | SQLAlchemy 2.0 | MySQL 驱动 |
| LLM 编排 | LangChain | 统一多厂商模型调用 |
| 数据库 | MySQL | 5.7+ |
| 模型接入 | Moonshot / DeepSeek / MiniMax / Ollama | 通过 langchain-openai 兼容 |

---

## 三、文件结构

```
学校创新实践/
├── index.html                     # 前端入口 HTML
├── package.json                   # 前端 npm 配置
├── vite.config.ts                 # Vite 构建配置
├── tsconfig.app.json              # TypeScript 应用配置（strict + noUnusedLocals）
├── openapi.yaml                   # 后端 API 规格（OpenAPI 3.0）
├── README.md                      # 项目说明
│
├── src/                           # 前端源码
│   ├── main.ts                    # 应用入口
│   ├── App.vue                    # 根组件
│   ├── style.css                  # 全局 Apple 风格 CSS 变量
│   ├── router/
│   │   └── index.ts               # 路由定义 + 导航守卫
│   ├── stores/
│   │   └── auth.ts                # Pinia 认证状态管理
│   ├── views/
│   │   ├── Login.vue              # 登录页
│   │   ├── Home.vue               # 首页
│   │   └── IntelligentAssistant.vue   # 智能助手核心页面（对话、模型选择、知识库、工具）
│   └── assets/                    # 静态资源
│
├── backend/                       # 后端服务（FastAPI）
│   ├── requirements.txt           # Python 依赖清单
│   ├── .env                       # 环境变量配置（数据库、API Key）
│   ├── init.sql                   # 数据库初始化 SQL
│   └── app/
│       ├── main.py                # FastAPI 应用入口
│       ├── config.py              # 配置管理（Pydantic Settings）
│       ├── database.py            # SQLAlchemy 数据库连接
│       ├── dependencies.py        # 依赖注入
│       ├── init_data.py           # 初始化数据脚本
│       ├── models/                # ORM 模型（user/conversation/message/term/alert）
│       ├── routers/               # API 路由（auth.py / assistant.py）
│       ├── schemas/               # Pydantic 数据模型
│       ├── services/              # 业务逻辑（llm / knowledge_base / weather_tool / conversation）
│       └── core/                  # 安全加密、SSE 封装
│
├── docs/                          # 项目文档
│   ├── project_spec.md            # 产品需求 + 工程设计规格
│   ├── architecture.md            # 架构文档
│   ├── project_status.md          # 项目状态与里程碑
│   └── changelog.md               # 变更日志
│
├── public/                        # 静态公共资源
├── dist/                          # 前端生产构建产物
└── .gitignore                     # Git 忽略规则
```

---

## 四、配置指南

### 4.1 数据库配置（MySQL）

创建数据库并执行初始化脚本：

```sql
CREATE DATABASE meteo_assistant CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

后端 `backend/init.sql` 包含完整建表语句，包含以下 5 张表：

| 表名 | 说明 |
|------|------|
| `users` | 用户表（用户名、bcrypt 密码哈希） |
| `conversations` | 对话表（UUID 主键、用户外键、模型 ID、标题） |
| `messages` | 消息表（角色、内容、工具调用 JSON） |
| `terms` | 气象术语库（术语名、分类、释义、来源） |
| `alerts` | 预警信号库（类型、级别、发布标准、防御指南） |

### 4.2 后端环境变量（`backend/.env`）

```bash
# 数据库（必配）
DATABASE_URL=mysql+pymysql://用户名:密码@localhost:3306/meteo_assistant

# LLM API Keys（至少配一个）
KIMI_API_KEY=sk-xxxxxxxx
DEEPSEEK_API_KEY=sk-xxxxxxxx
MINIMAX_API_KEY=xxxxxxxx

# 天气搜索工具（必配）
TAVILY_API_KEY=tvly-xxxxxxxx

# 实时预警（可选，未配置时 fallback 到数据库）
QWEATHER_API_KEY=xxxxxxxx

# 本地模型（可选）
OLLAMA_BASE_URL=http://localhost:11434/v1

# 应用配置
APP_SECRET_KEY=your-secret-key-change-in-production
ALLOWED_ORIGINS=http://localhost:5173
```

### 4.3 前端环境

前端无额外环境变量配置，直接依赖 `vite.config.ts` 中的代理设置，开发时请求自动转发到 `http://localhost:8000`。

---

## 五、启动步骤

### 5.1 启动后端

```bash
# 1. 进入后端目录
cd backend

# 2. 创建虚拟环境（首次）
python -m venv venv

# 3. 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. 安装依赖（首次）
pip install -r requirements.txt

# 5. 初始化数据库（首次）
# 在 MySQL 中执行 init.sql 建表，然后运行：
python -c "from app.init_data import init_data; init_data()"

# 6. 启动服务
uvicorn app.main:app --reload --port 8000
```

后端启动后，API 文档地址：`http://localhost:8000/docs`

### 5.2 启动前端

```bash
# 1. 在项目根目录安装依赖（首次）
npm install

# 2. 启动开发服务器
npm run dev
```

前端默认地址：`http://localhost:5173`

### 5.3 生产构建

```bash
# 前端生产构建
npm run build
# 产物输出到 dist/ 目录
```

---

## 六、API 接口概览

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/auth/login` | 用户登录（Session-Cookie） |
| POST | `/api/v1/auth/logout` | 用户登出 |
| GET | `/api/v1/assistant/models` | 获取可用模型列表 |
| GET | `/api/v1/assistant/knowledge-bases` | 获取知识库列表 |
| GET | `/api/v1/assistant/tools` | 获取工具列表 |
| POST | `/api/v1/assistant/chat/stream` | 流式对话（SSE） |
| GET | `/api/v1/assistant/conversations` | 获取对话列表 |
| POST | `/api/v1/assistant/conversations` | 创建新对话 |
| GET | `/api/v1/assistant/conversations/{id}` | 获取对话详情 |
| PUT | `/api/v1/assistant/conversations/{id}` | 重命名对话 |
| DELETE | `/api/v1/assistant/conversations/{id}` | 删除对话 |

---

## 七、已实现功能清单

- [x] 用户登录 / 登出（Session-Cookie 认证）
- [x] 智能助手对话界面（流式输出、Markdown 渲染）
- [x] 多模型切换（Kimi K2.5 / DeepSeek Reasoner / MiniMax-M2.5 / Ollama 本地）
- [x] 对话历史管理（创建、切换、删除、重命名）
- [x] 气象术语知识库（SQL 查询注入 Prompt）
- [x] 预警信号知识库（QWeather 实时 API + 数据库 fallback）
- [x] 天气查询工具（Tavily 搜索 + 查询词增强）
- [x] 当前日期动态注入（System Prompt 自动追加）
- [x] 前端消息 Markdown 渲染 + 代码高亮
- [x] 响应式布局（Apple 风格设计）
