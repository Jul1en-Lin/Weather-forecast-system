from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user_from_request

def get_db_session(db: Session = Depends(get_db)) -> Session:
    return db

def get_current_user(user: dict = Depends(get_current_user_from_request)) -> dict:
    return user

def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    if not current_user.get("is_admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="需要管理员权限")
    return current_user
