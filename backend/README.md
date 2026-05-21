# 气象智能助手后端

## 技术栈

- **框架**：FastAPI + SQLAlchemy
- **数据库**：SQLite（无需安装，自动创建）
- **LLM 编排**：LangChain
- **认证**：Session-Cookie + bcrypt 密码哈希

## 启动

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## 环境变量

复制 `.env` 并填写真实值：

| 变量 | 说明 |
|------|------|
| `DATABASE_URL` | SQLite 连接串 |
| `KIMI_API_KEY` | Kimi 模型 API Key |
| `DEEPSEEK_API_KEY` | DeepSeek 模型 API Key |
| `MINIMAX_API_KEY` | MiniMax 模型 API Key |
| `TAVILY_API_KEY` | 天气搜索工具 Key |
| `QWEATHER_API_KEY` | 和风天气预警 API Key |
| `QWEATHER_API_HOST` | 和风天气 API 服务器地址 |
| `OLLAMA_BASE_URL` | Ollama 本地模型地址 |
| `ALLOWED_ORIGINS` | 前端地址，默认 `http://localhost:5173` |

## API 端点

### 认证相关
| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/auth/register` | POST | 用户注册 |
| `/api/v1/auth/login` | POST | 用户登录 |
| `/api/v1/auth/logout` | POST | 用户登出 |
| `/api/v1/auth/me` | GET | 获取当前用户信息（含 is_admin） |

### 用户管理（仅管理员）
| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/users/` | GET | 获取所有用户列表 |
| `/api/v1/users/me` | GET | 获取当前用户信息 |
| `/api/v1/users/{id}` | PUT | 更新用户（修改 is_admin） |
| `/api/v1/users/{id}` | DELETE | 删除用户 |

### 配置管理
| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/config/` | GET | 获取当前配置（敏感信息已掩码） |
| `/api/v1/config/` | PUT | 更新配置（所有已登录用户） |

### 智能助手
| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/assistant/models` | GET | 获取模型列表 |
| `/api/v1/assistant/knowledge-bases` | GET | 获取知识库列表 |
| `/api/v1/assistant/tools` | GET | 获取工具列表 |
| `/api/v1/assistant/chat/stream` | POST | 流式对话（SSE） |
| `/api/v1/assistant/conversations` | GET/POST | 对话管理 |
| `/api/v1/assistant/messages` | GET | 获取历史消息 |

## 数据库

SQLite 数据库文件：`database.sqlite`（自动创建）

用户表（users）字段：
- `id`: 主键
- `username`: 用户名（唯一）
- `password_hash`: bcrypt 加密密码
- `is_admin`: 是否管理员（默认 false）
- `created_at`: 创建时间
- `updated_at`: 更新时间

## API 文档

启动后访问：http://localhost:8000/docs
