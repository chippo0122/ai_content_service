
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.keyword import Keyword

class KeywordRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, keyword_id):
        return self.db.query(Keyword).filter(Keyword.id == keyword_id).first()

    def update_status(self, keyword_id, status):
        keyword = self.get_by_id(keyword_id)
        if keyword:
            keyword.status = status
            self.db.commit()
        return keyword

    def get_by_status(self, status):
        return self.db.query(Keyword).filter(Keyword.status == status).all()

    def get_recent(self, limit=20, offset=0):
        return self.db.query(Keyword).order_by(Keyword.id.desc()).offset(offset).limit(limit).all()

    def get_today_titles(self):
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        return set(
            row[0] for row in self.db.query(Keyword.title)
            .filter(Keyword.fetched_at >= today_start, Keyword.fetched_at <= today_end)
            .all()
        )

    def batch_add(self, keywords: list):
        now = datetime.utcnow()
        today_titles = self.get_today_titles()
        new_count = 0
        for kw in keywords:
            if kw["title"] in today_titles:
                continue
            self.db.add(Keyword(
                source=kw["source"],
                title=kw["title"],
                url=kw["url"],
                status=kw["status"],
                raw_data=kw["raw_data"],
                fetched_at=now
            ))
            today_titles.add(kw["title"])
            new_count += 1
        self.db.commit()
        return new_count
