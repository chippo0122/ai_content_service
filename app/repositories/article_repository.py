from sqlalchemy.orm import Session
from app.models.article import Article

class ArticleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs):
        article = Article(**kwargs)
        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)
        return article

    def get_by_status(self, status):
        return self.db.query(Article).filter(Article.status == status).all()

    def get_by_id(self, article_id):
        return self.db.query(Article).filter(Article.id == article_id).first()

    def update(self, article_id, **kwargs):
        article = self.get_by_id(article_id)
        if article:
            for k, v in kwargs.items():
                setattr(article, k, v)
            self.db.commit()
        return article
