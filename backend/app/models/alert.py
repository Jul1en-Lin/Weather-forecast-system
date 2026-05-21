from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.database import Base

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    alert_type = Column(String(50), nullable=False)
    level = Column(String(10), nullable=False)  # SQLite 不支持 ENUM，使用 String 存储
    criteria = Column(Text, nullable=False)
    response_guide = Column(Text)
    created_at = Column(DateTime, server_default=func.now())