from pydantic import BaseModel
from typing import Optional, List

class ToolConfigSchema(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    api_key: Optional[str] = None
    masked_api_key: Optional[str] = None
    api_host: Optional[str] = None

    class Config:
        from_attributes = True

class ToolConfigUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    api_key: Optional[str] = None
    api_host: Optional[str] = None

class ToolConfigListResponse(BaseModel):
    tools: List[ToolConfigSchema]
