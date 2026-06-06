from pydantic import BaseModel, Field
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
    model_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)
    conversation_id: Optional[str] = None
    knowledge_base_ids: Optional[List[str]] = None
    tool_ids: Optional[List[str]] = None

class WeatherCardRequest(BaseModel):
    city: str = Field(..., min_length=1)
    model_id: Optional[str] = None

class WeatherCardResponse(BaseModel):
    location: str
    weather_summary: str
    mood_title: str
    fortune_rating: str
    mood_analysis: str
    suggestion_yee: str
    suggestion_kee: str
