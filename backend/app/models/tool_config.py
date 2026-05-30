from sqlalchemy import Column, String, DateTime, func
from app.database import Base

class ToolConfig(Base):
    __tablename__ = "tool_configs"
    id = Column(String(64), primary_key=True)  # e.g., weather_query, alert_query
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    api_key = Column(String(255))
    api_host = Column(String(255))  # Specific to QWeather
    created_at = Column(DateTime, server_default=func.now())
