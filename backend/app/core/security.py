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
