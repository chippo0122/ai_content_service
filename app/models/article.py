from sqlalchemy import Column, String, Text, BigInteger, JSON, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.sql import func
from app.models import Base

class Article(Base):
    __tablename__ = "articles"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    keyword_id = Column(BigInteger, ForeignKey("keywords.id"), nullable=False)
    status = Column(VARCHAR(50), nullable=False)
    title = Column(VARCHAR(255), nullable=False)
    content = Column(Text, nullable=False)
    parameters = Column(JSON, nullable=True)
    ai_model_used = Column(VARCHAR(100), nullable=True)
    final_prompt = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
