from sqlalchemy import Column, Text, BigInteger, DateTime
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.sql import func
from app.models import Base

class Keyword(Base):
    __tablename__ = "keywords"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    source = Column(VARCHAR(50), nullable=False)
    title = Column(VARCHAR(255), nullable=False)
    url = Column(Text, nullable=True)
    hotness_score = Column(BigInteger, nullable=True)
    status = Column(VARCHAR(50), nullable=False, default="pending_selection")
    raw_data = Column(Text, nullable=True)
    fetched_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
