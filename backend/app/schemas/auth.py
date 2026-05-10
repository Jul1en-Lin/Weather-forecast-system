from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    username: str
    is_admin: bool

class MeResponse(BaseModel):
    username: str
    is_admin: bool
