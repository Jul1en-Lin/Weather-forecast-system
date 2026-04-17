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
