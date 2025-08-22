from sqlalchemy import Column, String, Text, BigInteger, JSON, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.sql import func
from app.models import Base

class ArticleGenerationLog(Base):
    __tablename__ = "article_generation_logs"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    keyword_id = Column(BigInteger, ForeignKey("keywords.id"), nullable=False)
    article_id = Column(BigInteger, ForeignKey("articles.id"), nullable=True)
    status = Column(VARCHAR(50), nullable=False)
    error_message = Column(Text, nullable=True)
    ai_model_used = Column(VARCHAR(100), nullable=True)
    final_prompt = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
