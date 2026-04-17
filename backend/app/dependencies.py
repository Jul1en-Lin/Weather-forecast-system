from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user_from_request

def get_db_session(db: Session = Depends(get_db)) -> Session:
    return db

def get_current_user(user: dict = Depends(get_current_user_from_request)) -> dict:
    return user
