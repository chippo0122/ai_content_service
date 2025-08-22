from sqlalchemy.orm import Session
from app.models.article_generation_log import ArticleGenerationLog

class LogRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs):
        log = ArticleGenerationLog(**kwargs)
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def get_by_keyword(self, keyword_id):
        return self.db.query(ArticleGenerationLog).filter(ArticleGenerationLog.keyword_id == keyword_id).all()
