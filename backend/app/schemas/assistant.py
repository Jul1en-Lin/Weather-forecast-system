from pydantic import BaseModel, Field
from typing import List, Optional

class ModelInfo(BaseModel):
    id: str
    name: str
    description: str

class ModelsResponse(BaseModel):
    models: List[ModelInfo]

class KnowledgeBaseInfo(BaseModel):
    id: str
    name: str
    description: str

class KnowledgeBasesResponse(BaseModel):
    knowledge_bases: List[KnowledgeBaseInfo]

class ToolInfo(BaseModel):
    id: str
    name: str
    description: str

class ToolsResponse(BaseModel):
    tools: List[ToolInfo]

class ChatStreamRequest(BaseModel):
    model_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)
    conversation_id: Optional[str] = None
    knowledge_base_ids: Optional[List[str]] = None
    tool_ids: Optional[List[str]] = None

class WeatherCardRequest(BaseModel):
    city: str = Field(..., min_length=1)
    model_id: Optional[str] = None
    tarot_card_id: Optional[str] = None

class WeatherOracleWeather(BaseModel):
    temperature: Optional[int] = None
    humidity: Optional[int] = None
    pressure: Optional[int] = None
    wind_speed: Optional[int] = None
    wind_direction: str = ""
    condition: str = ""
    observed_at: str = ""


class WeatherOracleTarot(BaseModel):
    id: str
    name_en: str
    name_zh: str
    image: str
    keywords: List[str]


class WeatherOracleFortune(BaseModel):
    title: str
    summary: str
    lucky_color: str
    lucky_number: int
    good_for: str
    avoid: str


class WeatherOracleMoodGuide(BaseModel):
    title: str
    analysis: str
    suggestions: List[str]


class WeatherOracleDailyAdvice(BaseModel):
    travel: str
    clothing: str


class WeatherOracleMapping(BaseModel):
    metric: str
    label: str
    value: str
    reading: str
    score: int


class WeatherOracleTip(BaseModel):
    title: str
    advice: str


class WeatherCardResponse(BaseModel):
    city: str
    date: str
    timezone: str
    updated_at: str
    weather: WeatherOracleWeather
    tarot: WeatherOracleTarot
    fortune: WeatherOracleFortune
    mood_guide: WeatherOracleMoodGuide
    daily_advice: WeatherOracleDailyAdvice
    weather_mappings: List[WeatherOracleMapping]
    weather_tip: Optional[WeatherOracleTip] = None
