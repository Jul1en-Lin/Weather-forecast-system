# MySQL → SQLite 迁移计划

> 参照 `docs4Dev/mysql-to-sqlite-migration-guide.md`，将本项目的后端数据库从 MySQL 迁移到 SQLite。
> 本项目后端为 Python FastAPI + SQLAlchemy，与教程中的 Node.js + Express 不同，但核心迁移思路一致。

---

## 1. 项目现状分析

### 当前数据库架构

- **数据库**: MySQL 8.x，库名 `meteo_assistant`
- **连接方式**: SQLAlchemy + PyMySQL，URL = `mysql+pymysql://root:dd.159178280@localhost:3306/meteo_assistant`
- **ORM**: SQLAlchemy 2.0 declarative_base，5 个模型表

### 数据表清单

| 表名 | 模型文件 | MySQL 特性使用 | SQLite 适配要点 |
|------|---------|---------------|----------------|
| `users` | `models/user.py` | `DateTime + server_default=func.now() + onupdate=func.now()` | `onupdate` 不生效，需应用层处理 |
| `conversations` | `models/conversation.py` | `DateTime + server_default + onupdate + ForeignKey CASCADE` | 外键需 `PRAGMA foreign_keys=ON` |
| `messages` | `models/message.py` | `DateTime + JSON + ForeignKey CASCADE` | JSON → TEXT（SQLite 无原生 JSON） |
| `terms` | `models/term.py` | `DateTime + server_default=func.now()` | 直接兼容 |
| `alerts` | `models/alert.py` | `Enum("蓝","黄","橙","红") + DateTime` | Enum → VARCHAR/TEXT + Check约束 |

### 需修改的文件清单

| 文件路径 | 修改内容 |
|---------|---------|
| `backend/.env` | `DATABASE_URL` 从 mysql+pymysql 改为 sqlite:/// 相对路径 |
| `backend/app/config.py` | `database_url` 默认值改为 SQLite 路径 |
| `backend/app/database.py` | `create_engine` 适配 SQLite（去掉 pool_pre_ping，添加 PRAGMA） |
| `backend/app/models/user.py` | `onupdate=func.now()` → 应用层手动更新 `updated_at` |
| `backend/app/models/alert.py` | `Enum` → `String` + Check 约束（或纯 String） |
| `backend/app/models/conversation.py` | `onupdate` → 应用层处理 |
| `backend/app/models/message.py` | `JSON` → `Text`（SQLite 存储 JSON 为文本） |
| `backend/app/services/conversation.py` | 所有写操作需手动设置 `updated_at` |
| `backend/app/services/weather_tool.py` | `Alert.level` 字段从 Enum 比较改为 String 比较 |
| `backend/requirements.txt` | 移除 `pymysql`，移除 `cryptography`（MySQL 依赖） |
| `backend/init.sql` | 重写为 SQLite 语法 |
| `.gitignore` | 添加 `*.sqlite` |
| `docs/architecture.md` | 更新数据层描述 |
| `docs/changelog.md` | 记录本次迁移 |

### 不需要修改的文件

| 文件路径 | 原因 |
|---------|------|
| `backend/app/main.py` | 仅调用 `Base.metadata.create_all` 和 `init_db()`，与数据库方言无关 |
| `backend/app/routers/auth.py` | 通过 SQLAlchemy ORM 操作，不写原生 SQL |
| `backend/app/routers/assistant.py` | 通过 Service 层操作数据库，不直接写 SQL |
| `backend/app/dependencies.py` | 仅依赖注入，与数据库无关 |
| `backend/app/core/security.py` | 认证逻辑，与数据库无关 |
| `backend/app/core/sse.py` | SSE 流式，与数据库无关 |
| `backend/app/schemas/*.py` | Pydantic 模型，与数据库无关 |
| `backend/app/services/knowledge_base.py` | 通过 ORM 查询，SQLAlchemy 自动适配 |
| `backend/app/services/llm.py` | LLM 调用，与数据库无关 |
| `src/` (前端) | 通过 API 交互，不直接连数据库 |

---

## 2. 迁移步骤（按执行顺序）

### Step 1: 修改依赖配置

**2.1 修改 `backend/requirements.txt`**

- 移除 `pymysql>=1.1`（MySQL 驱动）
- 移除 `cryptography>=42.0`（PyMySQL 的依赖，仅 MySQL 需要）
- 无需添加新包：SQLAlchemy 内置支持 SQLite（使用 Python 标准库 `sqlite3`）

**2.2 修改 `backend/.env`**

- 将 `DATABASE_URL=mysql+pymysql://root:dd.159178280@localhost:3306/meteo_assistant`
- 改为 `DATABASE_URL=sqlite:///./database.sqlite`
- 数据库文件将位于 `backend/database.sqlite`

**2.3 修改 `backend/app/config.py`**

- `database_url` 默认值改为 `sqlite:///./database.sqlite`

### Step 2: 修改数据库连接模块

**修改 `backend/app/database.py`**

- `create_engine` 参数调整：
  - 去掉 `pool_pre_ping=True`（SQLite 不需要连接池健康检查）
  - 添加 `connect_args={"check_same_thread": False}`（SQLite 默认限制跨线程访问，FastAPI 多线程需放开）
  - 添加事件监听器，在连接时执行 `PRAGMA foreign_keys=ON`（SQLite 默认不启用外键约束）
  - 添加 `PRAGMA journal_mode=WAL`（提升并发读写性能）

### Step 3: 修改 ORM 模型（适配 SQLite 语法差异）

**3.1 修改 `backend/app/models/alert.py`**

- `Enum("蓝", "黄", "橙", "红", name="alert_level")` → `String(10)`
- SQLite 不支持 MySQL 的 ENUM 类型，改用 String 存储，业务层自行校验值范围
- 可选：添加 Check 约束 `Column(String(10), CheckConstraint("level IN ('蓝','黄','橙','红')"))`

**3.2 修改 `backend/app/models/message.py`**

- `Column(JSON, default=None)` → `Column(Text, default=None)`
- SQLite 无原生 JSON 类型，但 SQLAlchemy 的 `JSON` 类型在 SQLite 方言下会自动映射为 `Text` 并做序列化/反序列化
- **决策**：保持 `JSON` 类型不变，SQLAlchemy 会自动处理（存为 TEXT，读时反序列化）
- 这样代码无需改动，SQLAlchemy 兼容层已处理

**3.3 修改 `backend/app/models/user.py` 和 `conversation.py`**

- `onupdate=func.now()` 在 SQLite 下不生效（SQLite 不支持 `ON UPDATE CURRENT_TIMESTAMP`）
- **方案**：移除 `onupdate=func.now()`，在 Service 层写操作时手动设置 `updated_at = datetime.now()`
- `server_default=func.now()` 在 SQLite 下会生成 `CURRENT_TIMESTAMP`，SQLite 支持此语法，无需改动

### Step 4: 修改 Service 层（手动管理 updated_at）

**修改 `backend/app/services/conversation.py`**

- `ConversationService.rename()`：添加 `conv.updated_at = datetime.now()`
- `ConversationService.add_message()`：更新所属对话的 `updated_at`
- `ConversationService.create()`：无需改动（`server_default` 会自动设置）

### Step 5: 修改 weather_tool.py

**修改 `backend/app/services/weather_tool.py`**

- `_query_alerts()` 中 `Alert.level == level` 的比较：Enum → String 后，比较逻辑不变
- 无需额外修改，SQLAlchemy 会处理类型映射

### Step 6: 修改 init.sql

**重写 `backend/init.sql`**

- `AUTO_INCREMENT` → `AUTOINCREMENT`（或 `INTEGER PRIMARY KEY`）
- `VARCHAR(n)` → `TEXT`（SQLite 无长度限制）
- `ENUM(...)` → `TEXT` + `CHECK(level IN ('蓝','黄','橙','红'))`
- `DATETIME DEFAULT CURRENT_TIMESTAMP` → `TEXT DEFAULT CURRENT_TIMESTAMP`（SQLite 用 TEXT 存日期）
- `ON UPDATE CURRENT_TIMESTAMP` → 删除（SQLite 不支持）
- `JSON` → `TEXT`
- 删除 `CREATE DATABASE` 和 `USE` 语句（SQLite 不需要）

### Step 7: 修改 .gitignore

- 添加 `*.sqlite` 和 `*.sqlite-wal`、`*.sqlite-shm`

### Step 8: 更新文档

**8.1 更新 `docs/architecture.md`**

- 数据层描述：MySQL ORM → SQLite ORM
- 驱动：PyMySQL → Python 内置 sqlite3
- 新增架构决策记录

**8.2 更新 `docs/changelog.md`**

- 添加本次迁移记录

**8.3 更新 `docs/project_status.md`**

- 更新已完成工作

---

## 3. SQLite 特性注意事项

### 3.1 不需要单独启动数据库服务

- MySQL 需要先安装、启动 MySQL Server，创建数据库
- SQLite 数据库就是一个文件，应用启动时 SQLAlchemy 自动创建

### 3.2 外键约束需手动启用

- MySQL 默认启用外键约束
- SQLite 默认**不检查**外键，需在每次连接时执行 `PRAGMA foreign_keys=ON`

### 3.3 并发写入限制

- SQLite 同一时刻只有一个写入者（库级锁）
- 启用 WAL 模式可提升并发性能：`PRAGMA journal_mode=WAL`
- 本项目为小型应用，并发写入压力极低，无需额外处理

### 3.4 数据库文件备份

- 直接复制 `database.sqlite` 文件即可
- 或使用 `sqlite3 database.sqlite ".backup 'backup.sqlite'"`

### 3.5 SQLAlchemy 自动适配

- SQLAlchemy 的 Dialect 系统会自动处理大部分 SQL 差异
- `JSON` 类型在 SQLite 下自动映射为 `Text` + 序列化/反序列化
- `DateTime` 在 SQLite 下存为 ISO 字符串
- `Enum` 在 SQLite 下存为 `VARCHAR`（但建表时不会加 CHECK 约束）

---

## 4. 验证计划

迁移完成后需验证：

1. **启动验证**：`uvicorn app.main:app --reload --port 8000` 能正常启动，`database.sqlite` 文件自动创建
2. **建表验证**：所有 5 张表正确创建，字段类型符合预期
3. **种子数据验证**：admin 用户、术语数据、预警数据正确插入
4. **CRUD 验证**：登录、创建对话、发送消息、查询对话列表等 API 正常工作
5. **外键验证**：删除用户时关联对话和消息被级联删除
6. **SSE 验证**：流式对话端点正常返回

---

## 5. 迁移优势总结

| 维度 | MySQL（迁移前） | SQLite（迁移后） |
|------|---------------|----------------|
| 安装 | 需安装 MySQL Server | 无需安装任何数据库服务 |
| 启动 | 需先启动 MySQL | `npm run dev` / `uvicorn` 即可 |
| 配置 | 需配置 host/port/user/password | 仅一个文件路径 |
| 部署 | 高复杂度 | 零复杂度（数据库就是一个文件） |
| 开发体验 | 需维护 MySQL 服务 | 完全自包含，开箱即用 |