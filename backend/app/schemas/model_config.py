from pydantic import BaseModel
from typing import Optional, List

class ModelConfigSchema(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    model: str
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    masked_api_key: Optional[str] = None
    temperature: Optional[float] = 0.7
    supports_tools: Optional[bool] = True
    is_local: Optional[bool] = False

    class Config:
        from_attributes = True

class ModelConfigCreate(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    model: str
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    temperature: Optional[float] = 0.7
    supports_tools: Optional[bool] = True
    is_local: Optional[bool] = False

class ModelConfigUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    model: Optional[str] = None
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    temperature: Optional[float] = None
    supports_tools: Optional[bool] = None
    is_local: Optional[bool] = None

class ModelConfigListResponse(BaseModel):
    models: List[ModelConfigSchema]
