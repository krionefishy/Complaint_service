from pydantic import BaseModel
from app.core.database import db
from sqlalchemy import Column, Integer, String, DateTime
from enum import Enum
from datetime import datetime, timezone


Base = db.Base

class FeedbackCategory(str, Enum):
    TECHNICAL = "техническая"
    PAYMENT = "оплата"
    OTHER = "другое"
    

class FeedbackStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"


class FeedbackSentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    UNKNOWN = "unknown"


class Feedback(Base):
    __tablename__ = "feedbacks"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text = Column(String(1000), nullable = False)
    status = Column(String(10), default=FeedbackStatus.OPEN)
    sentiment = Column(String(20), default=FeedbackSentiment.UNKNOWN)
    category = Column(String(20), default=FeedbackCategory.OTHER)
    timestamp = Column(DateTime, default= lambda: datetime.now(timezone.utc))
    

class FeedbackCreate(BaseModel):
    text: str


class FeedbackResponse(BaseModel):
    id: int
    text: str
    status: str
    sentiment: str 
    category: str
    timestamp: datetime


class SentimentResponse(BaseModel):
    text: str
    sentiment: FeedbackSentiment

class TypeResponse(BaseModel):
    text: str
    category: FeedbackCategory


