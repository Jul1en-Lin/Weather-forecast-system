from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)
    password: str = Field(..., min_length=6, max_length=128)

class UserResponse(BaseModel):
    id: int
    username: str
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    is_admin: Optional[bool] = None

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)
    password: str = Field(..., min_length=6, max_length=128)

class RegisterResponse(BaseModel):
    id: int
    username: str
    is_admin: bool