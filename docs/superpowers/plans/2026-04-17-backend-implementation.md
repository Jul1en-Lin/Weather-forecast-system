# 后端实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 基于 `docs/project_spec.md` 构建完整的 FastAPI 后端，为前端提供认证、对话管理、SSE 流式对话、知识库注入、天气工具调用等能力。

**Architecture:** FastAPI + SQLAlchemy (MySQL) + LangChain (langchain-openai / langchain-tavily) + 内存 Session-Cookie 认证。按功能模块逐个实现，从骨架到核心流式对话。

**Tech Stack:** Python 3.10+, FastAPI, Uvicorn, SQLAlchemy, PyMySQL, bcrypt, langchain, langchain-openai, langchain-tavily

---

## 文件结构映射

| 文件 | 职责 |
|------|------|
| `backend/requirements.txt` | Python 依赖 |
| `backend/.env` | 环境变量模板 |
| `backend/app/config.py` | Pydantic Settings 读取 .env |
| `backend/app/database.py` | SQLAlchemy engine、session、表创建 |
| `backend/app/dependencies.py` | DB Session、当前用户依赖 |
| `backend/app/core/security.py` | bcrypt 哈希、内存 session 管理 |
| `backend/app/core/sse.py` | SSE StreamingResponse 辅助 |
| `backend/app/models/*.py` | 5 张表的 ORM 模型 |
| `backend/app/schemas/*.py` | Pydantic 请求/响应模型 |
| `backend/app/routers/auth.py` | /login /logout /me |
| `backend/app/routers/assistant.py` | /api/v1/assistant/* 全部路由 |
| `backend/app/services/conversation.py` | 对话 CRUD、上下文组装 |
| `backend/app/services/llm.py` | ChatOpenAI 初始化、模型映射、流式调用 |
| `backend/app/services/knowledge_base.py` | 知识库 SQL 查询与 prompt 注入 |
| `backend/app/services/weather_tool.py` | TavilySearch 封装 |
| `backend/app/main.py` | FastAPI 应用入口、路由注册、CORS |

---

### Task 1: 项目骨架与依赖

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/.env`
- Create: `backend/app/__init__.py`
- Create: `backend/app/config.py`
- Create: `backend/app/database.py`

- [ ] **Step 1: 创建 requirements.txt**

```txt
fastapi>=0.110
uvicorn[standard]>=0.27
sqlalchemy>=2.0
pymysql>=1.1
bcrypt>=4.0
pydantic>=2.0
pydantic-settings>=2.0
langchain>=0.1
langchain-openai>=0.1
langchain-tavily>=0.1
python-multipart>=0.0.9
```

- [ ] **Step 2: 创建 .env 模板**

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

- [ ] **Step 3: 创建 app/__init__.py**

```python
# backend/app/__init__.py
```

- [ ] **Step 4: 创建 config.py**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    kimi_api_key: str = ""
    deepseek_api_key: str = ""
    minimax_api_key: str = ""
    tavily_api_key: str = ""
    ollama_base_url: str = "http://localhost:11434/v1"
    app_secret_key: str = "change-me"
    allowed_origins: str = "http://localhost:5173"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

- [ ] **Step 5: 创建 database.py**

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- [ ] **Step 6: 提交**

```bash
git add backend/
git commit -m "chore: backend skeleton, config, database setup

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 2: 核心工具（Security + SSE + Dependencies）

**Files:**
- Create: `backend/app/core/__init__.py`
- Create: `backend/app/core/security.py`
- Create: `backend/app/core/sse.py`
- Create: `backend/app/dependencies.py`

- [ ] **Step 1: 创建 core/__init__.py**

```python
# backend/app/core/__init__.py
```

- [ ] **Step 2: 创建 security.py**

```python
import secrets
import bcrypt
from fastapi import Request, HTTPException, status

# 内存 session 存储: {session_id: {"user_id": int, "username": str}}
_session_store: dict[str, dict] = {}

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

def create_session(user_id: int, username: str) -> str:
    session_id = secrets.token_urlsafe(32)
    _session_store[session_id] = {"user_id": user_id, "username": username}
    return session_id

def delete_session(session_id: str) -> None:
    _session_store.pop(session_id, None)

def get_session(session_id: str | None) -> dict | None:
    if not session_id:
        return None
    return _session_store.get(session_id)

def get_current_user_from_request(request: Request) -> dict:
    session_id = request.cookies.get("session_id")
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return session
```

- [ ] **Step 3: 创建 sse.py**

```python
from fastapi.responses import StreamingResponse
import json

class SSEStream:
    @staticmethod
    def event(data: dict | str) -> str:
        if isinstance(data, dict):
            payload = json.dumps(data, ensure_ascii=False)
        else:
            payload = data
        return f"data: {payload}\n\n"

def sse_response(generator):
    return StreamingResponse(generator, media_type="text/event-stream", headers={
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no",
    })
```

- [ ] **Step 4: 创建 dependencies.py**

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user_from_request

def get_db_session(db: Session = Depends(get_db)) -> Session:
    return db

def get_current_user(user: dict = Depends(get_current_user_from_request)) -> dict:
    return user
```

- [ ] **Step 5: 提交**

```bash
git add backend/app/core/ backend/app/dependencies.py
git commit -m "feat: add security, sse, dependencies core modules

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 3: 数据模型（ORM）

**Files:**
- Create: `backend/app/models/__init__.py`
- Create: `backend/app/models/user.py`
- Create: `backend/app/models/conversation.py`
- Create: `backend/app/models/message.py`
- Create: `backend/app/models/term.py`
- Create: `backend/app/models/alert.py`

- [ ] **Step 1: 创建 models/__init__.py**

```python
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.term import Term
from app.models.alert import Alert

__all__ = ["User", "Conversation", "Message", "Term", "Alert"]
```

- [ ] **Step 2: 创建 user.py**

```python
from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
```

- [ ] **Step 3: 创建 conversation.py**

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(String(36), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), default="新对话")
    model_id = Column(String(64), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
```

- [ ] **Step 4: 创建 message.py**

```python
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String(36), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant, system, tool
    content = Column(Text, nullable=False)
    tool_calls = Column(JSON, default=None)
    created_at = Column(DateTime, server_default=func.now())
    conversation = relationship("Conversation", back_populates="messages")
```

- [ ] **Step 5: 创建 term.py**

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.database import Base

class Term(Base):
    __tablename__ = "terms"
    id = Column(Integer, primary_key=True, autoincrement=True)
    term = Column(String(100), nullable=False)
    category = Column(String(50))
    definition = Column(Text, nullable=False)
    source = Column(String(200))
    created_at = Column(DateTime, server_default=func.now())
```

- [ ] **Step 6: 创建 alert.py**

```python
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, func
from app.database import Base

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    alert_type = Column(String(50), nullable=False)
    level = Column(Enum("蓝", "黄", "橙", "红", name="alert_level"), nullable=False)
    criteria = Column(Text, nullable=False)
    response_guide = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
```

- [ ] **Step 7: 提交**

```bash
git add backend/app/models/
git commit -m "feat: add SQLAlchemy ORM models (user, conversation, message, term, alert)

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 4: Pydantic Schemas

**Files:**
- Create: `backend/app/schemas/__init__.py`
- Create: `backend/app/schemas/auth.py`
- Create: `backend/app/schemas/assistant.py`
- Create: `backend/app/schemas/conversation.py`

- [ ] **Step 1: 创建 schemas/__init__.py**

```python
# backend/app/schemas/__init__.py
```

- [ ] **Step 2: 创建 auth.py**

```python
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    username: str

class MeResponse(BaseModel):
    username: str
```

- [ ] **Step 3: 创建 assistant.py**

```python
from pydantic import BaseModel
from typing import List, Optional

class ModelInfo(BaseModel):
    id: str
    name: str
    description: str

class ModelsResponse(BaseModel):
    models: List[ModelInfo]

class KnowledgeBaseInfo(BaseModel):
    id: str
    name: str
    description: str

class KnowledgeBasesResponse(BaseModel):
    knowledge_bases: List[KnowledgeBaseInfo]

class ToolInfo(BaseModel):
    id: str
    name: str
    description: str

class ToolsResponse(BaseModel):
    tools: List[ToolInfo]

class ChatStreamRequest(BaseModel):
    model_id: str
    message: str
    conversation_id: Optional[str] = None
    knowledge_base_ids: Optional[List[str]] = None
    tool_ids: Optional[List[str]] = None

class SpeechToTextResponse(BaseModel):
    text: str
```

- [ ] **Step 4: 创建 conversation.py**

```python
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MessageItem(BaseModel):
    role: str
    content: str
    created_at: Optional[datetime] = None

class ConversationItem(BaseModel):
    id: str
    title: str
    model_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ConversationDetail(BaseModel):
    id: str
    title: str
    model_id: str
    messages: List[MessageItem]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ConversationsResponse(BaseModel):
    conversations: List[ConversationItem]
    total: int

class CreateConversationRequest(BaseModel):
    title: Optional[str] = "新对话"
    model_id: str

class RenameConversationRequest(BaseModel):
    title: str

class BatchDeleteRequest(BaseModel):
    conversation_ids: List[str]
```

- [ ] **Step 5: 提交**

```bash
git add backend/app/schemas/
git commit -m "feat: add Pydantic schemas for auth, assistant, conversation

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 5: 认证路由（Auth Router）

**Files:**
- Create: `backend/app/routers/__init__.py`
- Create: `backend/app/routers/auth.py`

- [ ] **Step 1: 创建 routers/__init__.py**

```python
# backend/app/routers/__init__.py
```

- [ ] **Step 2: 创建 auth.py**

```python
from fastapi import APIRouter, Request, Response, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db_session, get_current_user
from app.models.user import User
from app.core.security import hash_password, verify_password, create_session, delete_session
from app.schemas.auth import LoginRequest, LoginResponse, MeResponse

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, response: Response, db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    session_id = create_session(user.id, user.username)
    response.set_cookie(key="session_id", value=session_id, httponly=True, samesite="lax", path="/")
    return LoginResponse(username=user.username)

@router.post("/logout")
def logout(response: Response, request: Request):
    session_id = request.cookies.get("session_id")
    if session_id:
        delete_session(session_id)
    response.delete_cookie(key="session_id", path="/")
    return {"detail": "Logged out"}

@router.get("/me", response_model=MeResponse)
def me(current_user: dict = Depends(get_current_user)):
    return MeResponse(username=current_user["username"])
```

- [ ] **Step 3: 提交**

```bash
git add backend/app/routers/auth.py
git commit -m "feat: add auth router (login, logout, me) with session-cookie

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 6: 对话服务（Conversation Service）

**Files:**
- Create: `backend/app/services/__init__.py`
- Create: `backend/app/services/conversation.py`

- [ ] **Step 1: 创建 services/__init__.py**

```python
# backend/app/services/__init__.py
```

- [ ] **Step 2: 创建 services/conversation.py**

```python
import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.conversation import Conversation
from app.models.message import Message

class ConversationService:
    @staticmethod
    def create(db: Session, user_id: int, title: str, model_id: str) -> Conversation:
        conv = Conversation(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title=title or "新对话",
            model_id=model_id,
        )
        db.add(conv)
        db.commit()
        db.refresh(conv)
        return conv

    @staticmethod
    def list_by_user(db: Session, user_id: int, page: int = 1, page_size: int = 20) -> tuple[List[Conversation], int]:
        query = db.query(Conversation).filter(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    @staticmethod
    def get(db: Session, conversation_id: str, user_id: int) -> Optional[Conversation]:
        return db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        ).first()

    @staticmethod
    def rename(db: Session, conversation_id: str, user_id: int, title: str) -> Optional[Conversation]:
        conv = ConversationService.get(db, conversation_id, user_id)
        if conv:
            conv.title = title
            db.commit()
            db.refresh(conv)
        return conv

    @staticmethod
    def delete(db: Session, conversation_id: str, user_id: int) -> bool:
        conv = ConversationService.get(db, conversation_id, user_id)
        if conv:
            db.delete(conv)
            db.commit()
            return True
        return False

    @staticmethod
    def batch_delete(db: Session, conversation_ids: List[str], user_id: int) -> int:
        deleted = db.query(Conversation).filter(
            Conversation.id.in_(conversation_ids),
            Conversation.user_id == user_id,
        ).delete(synchronize_session=False)
        db.commit()
        return deleted

    @staticmethod
    def get_messages(db: Session, conversation_id: str, user_id: int) -> List[Message]:
        conv = ConversationService.get(db, conversation_id, user_id)
        if not conv:
            return []
        return db.query(Message).filter(
            Message.conversation_id == conversation_id,
        ).order_by(Message.created_at.asc()).all()

    @staticmethod
    def add_message(db: Session, conversation_id: str, role: str, content: str, tool_calls: Optional[dict] = None) -> Message:
        msg = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            tool_calls=tool_calls,
        )
        db.add(msg)
        db.commit()
        db.refresh(msg)
        return msg
```

- [ ] **Step 3: 提交**

```bash
git add backend/app/services/conversation.py
git commit -m "feat: add conversation service (CRUD, messages)

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 7: 助手路由 — 对话管理、模型列表、知识库、工具

**Files:**
- Create: `backend/app/routers/assistant.py`
- Modify: `backend/app/main.py`（注册路由，见 Task 10）

- [ ] **Step 1: 创建 assistant.py 的非流式部分**

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db_session, get_current_user
from app.services.conversation import ConversationService
from app.schemas.assistant import (
    ModelsResponse, ModelInfo,
    KnowledgeBasesResponse, KnowledgeBaseInfo,
    ToolsResponse, ToolInfo,
    ChatStreamRequest,
    SpeechToTextResponse,
)
from app.schemas.conversation import (
    ConversationsResponse, ConversationItem,
    ConversationDetail, MessageItem,
    CreateConversationRequest, RenameConversationRequest,
    BatchDeleteRequest,
)

router = APIRouter(prefix="/api/v1/assistant", tags=["assistant"])

# ---- 模型列表 ----
@router.get("/models", response_model=ModelsResponse)
def get_models():
    return ModelsResponse(models=[
        ModelInfo(id="kimi-k2.5", name="Kimi K2.5", description="Moonshot 高性能模型"),
        ModelInfo(id="MiniMax-M2.5", name="MiniMax M2.5", description="MiniMax 通用模型"),
        ModelInfo(id="deepseek-reasoner", name="DeepSeek Reasoner", description="DeepSeek 推理模型"),
        ModelInfo(id="deepseek-r1:14b", name="DeepSeek R1 14B (本地)", description="Ollama 本地模型"),
    ])

# ---- 知识库列表 ----
@router.get("/knowledge-bases", response_model=KnowledgeBasesResponse)
def get_knowledge_bases():
    return KnowledgeBasesResponse(knowledge_bases=[
        KnowledgeBaseInfo(id="kb_weather", name="气象术语库", description="气象专业术语释义"),
        KnowledgeBaseInfo(id="kb_alert", name="预警信号库", description="气象预警信号标准与防御指南"),
    ])

# ---- 工具列表 ----
@router.get("/tools", response_model=ToolsResponse)
def get_tools():
    return ToolsResponse(tools=[
        ToolInfo(id="weather_query", name="天气查询", description="查询实时天气信息"),
        ToolInfo(id="alert_query", name="预警查询", description="查询气象预警信号"),
    ])

# ---- 对话管理 ----
@router.get("/conversations", response_model=ConversationsResponse)
def list_conversations(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    items, total = ConversationService.list_by_user(db, current_user["user_id"], page, page_size)
    return ConversationsResponse(
        conversations=[
            ConversationItem(
                id=c.id,
                title=c.title,
                model_id=c.model_id,
                created_at=c.created_at,
                updated_at=c.updated_at,
            ) for c in items
        ],
        total=total,
    )

@router.post("/conversations", response_model=ConversationItem)
def create_conversation(
    req: CreateConversationRequest,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    conv = ConversationService.create(db, current_user["user_id"], req.title, req.model_id)
    return ConversationItem(
        id=conv.id,
        title=conv.title,
        model_id=conv.model_id,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
    )

@router.get("/conversations/{conversation_id}", response_model=ConversationDetail)
def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    conv = ConversationService.get(db, conversation_id, current_user["user_id"])
    if not conv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    messages = ConversationService.get_messages(db, conversation_id, current_user["user_id"])
    return ConversationDetail(
        id=conv.id,
        title=conv.title,
        model_id=conv.model_id,
        messages=[
            MessageItem(role=m.role, content=m.content, created_at=m.created_at)
            for m in messages
        ],
        created_at=conv.created_at,
        updated_at=conv.updated_at,
    )

@router.put("/conversations/{conversation_id}", response_model=ConversationItem)
def rename_conversation(
    conversation_id: str,
    req: RenameConversationRequest,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    conv = ConversationService.rename(db, conversation_id, current_user["user_id"], req.title)
    if not conv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    return ConversationItem(
        id=conv.id,
        title=conv.title,
        model_id=conv.model_id,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
    )

@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    ok = ConversationService.delete(db, conversation_id, current_user["user_id"])
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    return {"detail": "Deleted"}

@router.post("/conversations/batch-delete")
def batch_delete_conversations(
    req: BatchDeleteRequest,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    count = ConversationService.batch_delete(db, req.conversation_ids, current_user["user_id"])
    return {"detail": f"Deleted {count} conversations"}

# ---- 语音转文字（预留） ----
@router.post("/speech-to-text", response_model=SpeechToTextResponse)
def speech_to_text():
    return SpeechToTextResponse(text="")
```

- [ ] **Step 2: 提交**

```bash
git add backend/app/routers/assistant.py
git commit -m "feat: add assistant router (models, kb, tools, conversation CRUD)

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 8: LLM 服务与模型配置

**Files:**
- Create: `backend/app/services/llm.py`

- [ ] **Step 1: 创建 llm.py**

```python
import os
from typing import Optional, AsyncIterator
from langchain_openai import ChatOpenAI
from app.config import settings

MODEL_CONFIG = {
    "kimi-k2.5": {
        "model": "kimi-k2.5",
        "base_url": "https://api.moonshot.cn/v1",
        "api_key": settings.kimi_api_key,
    },
    "deepseek-reasoner": {
        "model": "deepseek-reasoner",
        "base_url": "https://api.deepseek.com/v1",
        "api_key": settings.deepseek_api_key,
    },
    "MiniMax-M2.5": {
        "model": "MiniMax-M2.5",
        "base_url": "https://api.minimax.chat/v1",
        "api_key": settings.minimax_api_key,
    },
    "deepseek-r1:14b": {
        "model": "deepseek-r1:14b",
        "base_url": settings.ollama_base_url,
        "api_key": "ollama",  # Ollama 需要任意非空字符串
    },
}

def get_llm(model_id: str, temperature: float = 0.7, streaming: bool = True) -> ChatOpenAI:
    config = MODEL_CONFIG.get(model_id)
    if not config:
        raise ValueError(f"Unknown model_id: {model_id}")
    return ChatOpenAI(
        model=config["model"],
        base_url=config["base_url"],
        api_key=config["api_key"],
        temperature=temperature,
        streaming=streaming,
    )

async def stream_llm_response(llm: ChatOpenAI, messages: list) -> AsyncIterator[str]:
    """Yield text chunks from LLM stream."""
    async for chunk in llm.astream(messages):
        content = chunk.content if hasattr(chunk, "content") else ""
        if content:
            yield content
```

- [ ] **Step 2: 提交**

```bash
git add backend/app/services/llm.py
git commit -m "feat: add LLM service with model mapping and streaming

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 9: 知识库服务与天气工具服务

**Files:**
- Create: `backend/app/services/knowledge_base.py`
- Create: `backend/app/services/weather_tool.py`

- [ ] **Step 1: 创建 knowledge_base.py**

```python
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.term import Term
from app.models.alert import Alert

class KnowledgeBaseService:
    @staticmethod
    def build_context(db: Session, knowledge_base_ids: Optional[List[str]]) -> str:
        if not knowledge_base_ids:
            return ""
        parts: List[str] = []
        if "kb_weather" in knowledge_base_ids:
            terms = db.query(Term).limit(20).all()
            if terms:
                parts.append("【气象术语库】")
                for t in terms:
                    parts.append(f"- {t.term}（{t.category or '通用'}）: {t.definition}")
        if "kb_alert" in knowledge_base_ids:
            alerts = db.query(Alert).limit(20).all()
            if alerts:
                parts.append("【预警信号库】")
                for a in alerts:
                    parts.append(f"- {a.alert_type}{a.level}预警: 标准={a.criteria}; 防御={a.response_guide or '无'}")
        return "\n".join(parts)
```

- [ ] **Step 2: 创建 weather_tool.py**

```python
from typing import Optional
from langchain_tavily import TavilySearch
from app.config import settings

class WeatherToolService:
    @staticmethod
    def get_tool():
        if not settings.tavily_api_key:
            return None
        return TavilySearch(
            tavily_api_key=settings.tavily_api_key,
            max_results=3,
            search_depth="basic",
        )

    @staticmethod
    def format_tool_result(result) -> str:
        """Format TavilySearch result for LLM prompt."""
        if hasattr(result, "content"):
            return str(result.content)
        return str(result)
```

- [ ] **Step 3: 提交**

```bash
git add backend/app/services/knowledge_base.py backend/app/services/weather_tool.py
git commit -m "feat: add knowledge base and weather tool services

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 10: 流式对话路由（核心 SSE）

**Files:**
- Modify: `backend/app/routers/assistant.py` — 追加 `/chat/stream` 端点

- [ ] **Step 1: 在 assistant.py 顶部追加 import**

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import asyncio
import json
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from app.dependencies import get_db_session, get_current_user
from app.services.conversation import ConversationService
from app.services.llm import get_llm, stream_llm_response
from app.services.knowledge_base import KnowledgeBaseService
from app.services.weather_tool import WeatherToolService
from app.core.sse import sse_response, SSEStream
from app.schemas.assistant import (
    ModelsResponse, ModelInfo,
    KnowledgeBasesResponse, KnowledgeBaseInfo,
    ToolsResponse, ToolInfo,
    ChatStreamRequest,
    SpeechToTextResponse,
)
from app.schemas.conversation import (
    ConversationsResponse, ConversationItem,
    ConversationDetail, MessageItem,
    CreateConversationRequest, RenameConversationRequest,
    BatchDeleteRequest,
)
```

- [ ] **Step 2: 在 assistant.py 末尾追加 /chat/stream 端点**

```python
@router.post("/chat/stream")
async def chat_stream(
    req: ChatStreamRequest,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["user_id"]

    # 确定/创建对话
    if req.conversation_id:
        conv = ConversationService.get(db, req.conversation_id, user_id)
        if not conv:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    else:
        conv = ConversationService.create(db, user_id, req.message[:30], req.model_id)

    conversation_id = conv.id

    # 保存用户消息
    ConversationService.add_message(db, conversation_id, "user", req.message)

    # 查询历史消息
    history_msgs = ConversationService.get_messages(db, conversation_id, user_id)

    # 构建 LangChain messages
    system_parts = ["你是一个专业的气象智能助手，帮助用户解答气象相关问题。"]

    # 知识库注入
    kb_context = KnowledgeBaseService.build_context(db, req.knowledge_base_ids)
    if kb_context:
        system_parts.append("以下是相关气象知识库内容，请结合这些内容回答：\n" + kb_context)

    lc_messages = [SystemMessage(content="\n".join(system_parts))]

    for m in history_msgs[:-1]:  # 排除刚添加的 user message（上面已加）
        if m.role == "user":
            lc_messages.append(HumanMessage(content=m.content))
        elif m.role == "assistant":
            lc_messages.append(AIMessage(content=m.content))

    lc_messages.append(HumanMessage(content=req.message))

    # 工具准备
    tools = []
    tool_service = None
    if req.tool_ids and "weather_query" in req.tool_ids:
        tool_service = WeatherToolService.get_tool()
        if tool_service:
            tools.append(tool_service)

    async def event_generator():
        assistant_content = ""
        try:
            llm = get_llm(req.model_id, streaming=True)

            if tools:
                # 两阶段稳妥方案
                bound_llm = llm.bind_tools(tools)
                first_response = await bound_llm.ainvoke(lc_messages)
                tool_calls = first_response.tool_calls if hasattr(first_response, "tool_calls") else []

                if tool_calls:
                    tool_messages = []
                    for tc in tool_calls:
                        tool_name = tc.get("name", "")
                        tool_args = tc.get("args", {})
                        if tool_service and tool_name == "tavily_search":
                            try:
                                query = tool_args.get("query", req.message)
                                search_result = await tool_service.ainvoke({"query": query})
                                result_text = WeatherToolService.format_tool_result(search_result)
                                tool_messages.append(result_text)
                            except Exception:
                                tool_messages.append("天气服务暂不可用，请稍后重试。")

                    # 构造最终 prompt
                    final_prompt_parts = ["\n".join(system_parts)]
                    final_prompt_parts.append("用户问题：" + req.message)
                    if tool_messages:
                        final_prompt_parts.append("工具查询结果：\n" + "\n".join(tool_messages))
                    final_prompt_parts.append("请根据以上信息回答用户。")

                    final_messages = [SystemMessage(content="\n".join(final_prompt_parts))]
                    async for chunk in llm.astream(final_messages):
                        text = chunk.content if hasattr(chunk, "content") else ""
                        if text:
                            assistant_content += text
                            yield SSEStream.event({"chunk": text})
                else:
                    # 无 tool_calls，直接流式输出 first_response 的 content
                    content = first_response.content if hasattr(first_response, "content") else ""
                    if content:
                        assistant_content += content
                        yield SSEStream.event({"chunk": content})
            else:
                # 无工具，直接流式
                async for chunk in stream_llm_response(llm, lc_messages):
                    assistant_content += chunk
                    yield SSEStream.event({"chunk": chunk})

        except Exception as e:
            error_msg = f"抱歉，服务暂时出现问题：{str(e)}"
            assistant_content += error_msg
            yield SSEStream.event({"chunk": error_msg})

        finally:
            # 保存助手消息
            db_local = SessionLocal()
            try:
                ConversationService.add_message(db_local, conversation_id, "assistant", assistant_content)
            finally:
                db_local.close()
            yield SSEStream.event("[DONE]")

    return sse_response(event_generator())
```

注意：`assistant.py` 顶部需要额外导入 `SessionLocal`：

```python
from app.database import SessionLocal
```

- [ ] **Step 3: 提交**

```bash
git add backend/app/routers/assistant.py
git commit -m "feat: add SSE streaming chat endpoint with LangChain + tools

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 11: FastAPI 主入口

**Files:**
- Create: `backend/app/main.py`

- [ ] **Step 1: 创建 main.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import auth, assistant
from app.config import settings

# 自动建表（开发阶段）
Base.metadata.create_all(bind=engine)

app = FastAPI(title="气象智能助手 API", version="1.0.0")

# CORS
origins = [origin.strip() for origin in settings.allowed_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由注册
app.include_router(auth.router)
app.include_router(assistant.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

- [ ] **Step 2: 提交**

```bash
git add backend/app/main.py
git commit -m "feat: FastAPI main entry with CORS and router registration

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 12: 启动脚本与 README

**Files:**
- Create: `backend/README.md`

- [ ] **Step 1: 创建 README.md**

```markdown
# 气象智能助手后端

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
- `DATABASE_URL`: MySQL 连接串
- `KIMI_API_KEY` / `DEEPSEEK_API_KEY` / `MINIMAX_API_KEY`: LLM API Key
- `TAVILY_API_KEY`: 天气搜索工具 Key
- `ALLOWED_ORIGINS`: 前端地址，默认 `http://localhost:5173`

## API 文档

启动后访问：http://localhost:8000/docs
```

- [ ] **Step 2: 提交**

```bash
git add backend/README.md
git commit -m "docs: add backend README with startup instructions

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 13: 初始化数据（默认用户）

**Files:**
- Create: `backend/app/init_data.py`

- [ ] **Step 1: 创建 init_data.py**

```python
from app.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password

def init_db():
    db = SessionLocal()
    try:
        # 创建默认测试用户 admin / admin123
        existing = db.query(User).filter(User.username == "admin").first()
        if not existing:
            user = User(
                username="admin",
                password_hash=hash_password("admin123"),
            )
            db.add(user)
            db.commit()
            print("Default user created: admin / admin123")
        else:
            print("Default user already exists")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
```

- [ ] **Step 2: 提交**

```bash
git add backend/app/init_data.py
git commit -m "chore: add default admin user init script

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 14: 验证与测试

- [ ] **Step 1: 安装依赖**

Run:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

- [ ] **Step 2: 初始化数据库和用户**

确保 MySQL 中已创建数据库 `meteo_assistant`，然后运行：
```bash
cd backend
python -m app.init_data
```
Expected: `Default user created: admin / admin123`

- [ ] **Step 3: 启动服务**

```bash
uvicorn app.main:app --reload --port 8000
```
Expected: `Uvicorn running on http://127.0.0.1:8000`

- [ ] **Step 4: 用 curl 测试登录**

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  -c cookies.txt -v
```
Expected: HTTP 200 + `Set-Cookie: session_id=...`

- [ ] **Step 5: 测试 me 接口**

```bash
curl http://localhost:8000/api/v1/auth/me -b cookies.txt
```
Expected: `{"username":"admin"}`

- [ ] **Step 6: 测试模型列表**

```bash
curl http://localhost:8000/api/v1/assistant/models -b cookies.txt
```
Expected: 4 个模型对象

- [ ] **Step 7: 测试创建对话**

```bash
curl -X POST http://localhost:8000/api/v1/assistant/conversations \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"title":"测试","model_id":"deepseek-reasoner"}'
```

- [ ] **Step 8: 测试流式对话**

```bash
curl -X POST http://localhost:8000/api/v1/assistant/chat/stream \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"model_id":"deepseek-reasoner","message":"今天北京天气怎么样？"}' \
  --no-buffer
```
Expected: SSE 流式输出 chunk，最后 `[DONE]`

- [ ] **Step 9: 提交**

```bash
git commit --allow-empty -m "test: backend smoke tests passed

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

## 自审结果

### Spec 覆盖检查
| Spec 需求 | 对应 Task |
|---------|----------|
| FR-001 Session-Cookie 认证 | Task 2 (security), Task 5 (auth router) |
| FR-002 流式对话 SSE | Task 8 (llm), Task 9 (kb/tool), Task 10 (chat stream) |
| FR-003 模型管理 | Task 7 (GET /models) |
| FR-004 知识库 SQL 注入 | Task 9 (knowledge_base.py), Task 10 |
| FR-005 天气工具 Tavily | Task 9 (weather_tool.py), Task 10 |
| FR-006 对话管理 CRUD | Task 6 (service), Task 7 (router) |
| FR-007 语音转文字预留 | Task 7 (空实现) |
| 数据库 Schema 5 张表 | Task 3 |
| SSE 格式规范 | Task 2 (sse.py), Task 10 |
| 环境变量 .env | Task 1 |
| 风险回退策略 | Task 10 (try/except, 工具降级) |

无遗漏。

### Placeholder 扫描
- 无 "TBD"、"TODO"、"implement later"
- 所有代码步骤均含完整代码
- 无 "add appropriate error handling" 等模糊描述
- 所有类型签名前后一致（model_id、conversation_id 等）

### 类型一致性
- `conversation_id` 全为 `str`
- `model_id` 全为 `str`
- `knowledge_base_ids` / `tool_ids` 全为 `Optional[List[str]]`
- Pydantic schema 与 ORM 字段对齐

---

## 执行方式选择

**Plan complete and saved to `docs/superpowers/plans/2026-04-17-backend-implementation.md`.**

**Two execution options:**

**1. Subagent-Driven (recommended)** — 每个 Task 派发给独立子代理执行，我在每两个 Task 之间审查代码质量，快速迭代，确保一致性。

**2. Inline Execution** — 在当前会话中逐个 Task 执行，批量推进，关键节点暂停审查。

**Which approach?**
