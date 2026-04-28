## 大语言模型气象业务应用平台


本项目是一款面向气象业务的大语言模型智能应用平台，采用前后端分离架构。

前端基于 Vue 3 提供智能气象问答对话界面；后端采用 Python + LangChain 技术，实现简单的天气检索功能，模型支持流式输出、知识库检索、调用天气工具等。

### 登录页
<img width="2825" height="1787" alt="login" src="https://github.com/user-attachments/assets/4aa8d82a-f5d3-4e6b-9adb-164792380541" />

### 首页
<img width="2824" height="1784" alt="home" src="https://github.com/user-attachments/assets/8ac0bf56-dae1-495a-b7c4-6bf24c9aa372" />
<img width="2824" height="1787" alt="AI-page" src="https://github.com/user-attachments/assets/f72ced63-9076-4cd9-8c93-6b45efe3e294" />

## 核心功能

- 智能对话模型：支持多轮对话上下文，SSE 流式输出，目前支持 4 个模型
- 知识库：分别拥有气象术语库、预警信号库，以 SQL 查询注入 Prompt 的方式增强回答
- 天气相关：天气实时查询（Tavily API）、气象预警查询（QWeather API）
- 对话管理：支持创建、切换、删除对话、历史消息持久化
- 状态保持：使用 Session-Cookie 存储用户状态
- Markdown：前端页面支持 Markdown 格式渲染

## 技术栈

- 前端：Vue 3 + Vite + TypeScript
- 后端： Python + LangChain + FastAPI
- 数据库：MySQL，用于存储对话记录与用户账号密码
- 模型 API 接入：目前支持 Kimi / DeepSeek / MiniMax / Ollama本地模型

## 文件结构

```
./
├── index.html                     # 前端入口 HTML
├── package.json                   # 前端 npm 配置
├── vite.config.ts                 # Vite 构建配置
├── tsconfig.app.json              # TypeScript 应用配置（strict + noUnusedLocals）
├── openapi.yaml                   # 后端 API 规格（OpenAPI 3.0）
├── README.md                      # 项目说明
│
├── src/                           # 前端源码
│   ├── main.ts                    # 应用入口
│   ├── App.vue                    # 相关组件
│   ├── style.css                  # 定义前端全局风格 CSS 变量
│   ├── router/
│   │   └── index.ts               # 路由
│   ├── stores/
│   │   └── auth.ts                # 用户认证状态管理
│   ├── views/
│   │   ├── Login.vue              # 登录页
│   │   ├── Home.vue               # 首页
│   │   └── IntelligentAssistant.vue   # 智能助手核心页面（对话、模型选择、知识库、工具）
│   └── assets/                    # 相关静态资源（如图片）
│
├── backend/                       # 后端服务
│   ├── requirements.txt           # Python 依赖清单
│   ├── .env                       # 环境变量配置（数据库、API Key）
│   ├── init.sql                   # 数据库初始化 SQL（位于 backend/ 目录下）
│   └── app/
│       ├── main.py                # FastAPI 应用入口
│       ├── config.py              # 配置管理（Pydantic Settings）
│       ├── database.py            # 数据库连接
│       ├── dependencies.py        # 保存相关依赖
│       ├── init_data.py           # 初始化数据的脚本
│       ├── models/                # 相关模型
│       ├── routers/               # API 路由
│       ├── schemas/               # Pydantic 数据，进行数据校验、类型转换、错误处理和数据序列化
│       ├── services/              # 后端服务（LLM 调用/ 调用天气工具 / 对话管理）
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
└── .gitignore                     
```


## 配置指南

### 数据库初始化配置

首先创建 meteo_assistant 数据库：

```sql
CREATE DATABASE IF NOT EXISTS meteo_assistant
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
```

用于初始化数据库的 sql 语句 `backend/init.sql` 包含完整建表语句，包含以下 5 张表，这 5 张表都存在 meteo_assistant 数据库中：

| 表名 | 必要说明 |
|------|------|
| `users` | 用户表（包含用户名、bcrypt 密码哈希字段） |
| `conversations` | 对话表（包含UUID 主键、用户外键、模型 ID、标题字段） |
| `messages` | 消息表（包含角色、内容、工具调用 JSON字段） |
| `terms` | 气象术语库（包含术语名、分类、释义、来源字段） |
| `alerts` | 预警信号库（包含类型、级别、发布标准、防御指南字段） |

- **手动执行**：手动执行 init.sql 语句进行初始化数据库与建表。
- **自动执行**：后端启动时会通过 SQLAlchemy 自动创建表。

### 数据入库

成功启动后端服务后会自动执行 init_db() 方法，初始化默认的账号密码并入库。具体操作在“启动步骤”章节可见

默认账号密码
admin
admin123

### 所需的环境变量（`backend/.env`）

```bash
# 数据库（在 DATABASE_URL 中填上你的用户名与密码，端口默认为 3306）
DATABASE_URL=mysql+pymysql://用户名:密码@localhost:3306/meteo_assistant

# LLM API Keys（至少配一个）
KIMI_API_KEY=sk-xxxxxxxx
DEEPSEEK_API_KEY=sk-xxxxxxxx
MINIMAX_API_KEY=xxxxxxxx

# 天气搜索工具（TAVILY 官网申请）
TAVILY_API_KEY=tvly-xxxxxxxx

# 实时预警（和风天气的预警 API，可选）
QWEATHER_API_KEY=xxxxxxxx

# Ollama 本地模型（端口默认为11434，可选）
OLLAMA_BASE_URL=http://localhost:11434/v1
```
前端无额外环境变量配置，直接依赖 `vite.config.ts` 中的代理设置，开发时请求自动转发到 `http://localhost:8000`。


## 启动步骤

### 启动后端

```bash
# 1. 进入后端目录
cd backend

# 2. 创建虚拟环境（首次）
python -m venv venv

# 3. 激活虚拟环境（首次）
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. 安装依赖（首次）
pip install -r requirements.txt

# 5. 初始化数据库（首次）
# 在 MySQL 中执行 init.sql 建表，然后运行（文件位于backend/init.sql）：
python -c "from app.init_data import init_data; init_data()"

# 6. 启动服务
uvicorn app.main:app --reload --port 8000
```
### 启动前端

```bash
# 1. 在项目根目录安装依赖（首次）
npm install

# 2. 启动服务器
npm run dev
```

启动成功后，可访问 API 文档地址查看接口 `http://localhost:8000/docs` 
<img width="2767" height="1770" alt="image" src="https://github.com/user-attachments/assets/5c61115d-65b5-4266-86ed-7b5e79de3f09" />

访问前端地址即可自动路由到登录页 `http://localhost:5173`
<img width="2825" height="1787" alt="login" src="https://github.com/user-attachments/assets/2b301bb9-b798-439a-9537-8f869aa3ac49" />
