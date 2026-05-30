from sqlalchemy import Column, String, Integer, Boolean, DateTime, func
from app.database import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String(128), primary_key=True)
    user_id = Column(Integer, nullable=False)
    username = Column(String(64), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
