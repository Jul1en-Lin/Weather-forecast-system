from sqlalchemy import Column, String, Float, Boolean, DateTime, func
from app.database import Base

class ModelConfig(Base):
    __tablename__ = "model_configs"
    id = Column(String(64), primary_key=True)  # unique string ID, e.g. kimi-k2.5
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    model = Column(String(100), nullable=False)  # model name parameter, e.g. kimi-k2.5
    base_url = Column(String(255))
    api_key = Column(String(255))
    temperature = Column(Float)
    supports_tools = Column(Boolean, default=True)
    is_local = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
