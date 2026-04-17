from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, func
from app.database import Base

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    alert_type = Column(String(50), nullable=False)
    level = Column(Enum("蓝", "黄", "橙", "红", name="alert_level"), nullable=False)
    criteria = Column(Text, nullable=False)
    response_guide = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
