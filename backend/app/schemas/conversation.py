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
