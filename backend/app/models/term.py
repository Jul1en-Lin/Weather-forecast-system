from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.database import Base

class Term(Base):
    __tablename__ = "terms"
    id = Column(Integer, primary_key=True, autoincrement=True)
    term = Column(String(100), nullable=False)
    category = Column(String(50))
    definition = Column(Text, nullable=False)
    source = Column(String(200))
    created_at = Column(DateTime, server_default=func.now())
