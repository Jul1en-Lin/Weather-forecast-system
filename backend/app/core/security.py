from __future__ import annotations

import secrets
import bcrypt
from fastapi import Request, HTTPException, status
from app.database import SessionLocal
from app.models.session import Session as UserSession

# 内存 session 存储: {session_id: {"user_id": int, "username": str, "is_admin": bool}}
_session_store: dict[str, dict] = {}

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

def create_session(user_id: int, username: str, is_admin: bool = False) -> str:
    session_id = secrets.token_urlsafe(32)
    session_data = {"user_id": user_id, "username": username, "is_admin": is_admin}
    _session_store[session_id] = session_data
    db = SessionLocal()
    try:
        db.merge(UserSession(id=session_id, **session_data))
        db.commit()
    finally:
        db.close()
    return session_id

def delete_session(session_id: str) -> None:
    _session_store.pop(session_id, None)
    db = SessionLocal()
    try:
        session = db.query(UserSession).filter(UserSession.id == session_id).first()
        if session:
            db.delete(session)
            db.commit()
    finally:
        db.close()

def get_session(session_id: str | None) -> dict | None:
    if not session_id:
        return None
    session = _session_store.get(session_id)
    if session:
        return session

    db = SessionLocal()
    try:
        persisted = db.query(UserSession).filter(UserSession.id == session_id).first()
        if not persisted:
            return None
        session = {
            "user_id": persisted.user_id,
            "username": persisted.username,
            "is_admin": persisted.is_admin,
        }
        _session_store[session_id] = session
        return session
    finally:
        db.close()

def get_current_user_from_request(request: Request) -> dict:
    session_id = request.cookies.get("session_id")
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return session
