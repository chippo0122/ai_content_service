
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.services.google_trends_rss_client import fetch_daily_google_trends, save_keywords_to_db
from app.core.db import get_db
from app.repositories import ArticleRepository
from app.repositories.keyword_repository import KeywordRepository
from app.core.celery_worker import generate_article_task

from fastapi import Body, HTTPException

app = FastAPI()

@app.get('/')
def root():
    return "Welcome to the AI Content Service! Ready to Develop"

# 新增 /keyword/db 端點（查詢資料庫）
@app.get("/keyword/db")
def get_keywords_from_db(db: Session = Depends(get_db), limit: int = 20, offset: int = 0):
    repo = KeywordRepository(db)
    keywords = repo.get_recent(limit=limit, offset=offset)
    return [
        {
            "id": k.id,
            "source": k.source,
            "title": k.title,
            "url": k.url,
            "hotness_score": getattr(k, "hotness_score", None),
            "status": k.status,
            "raw_data": k.raw_data,
            "fetched_at": k.fetched_at,
            "created_at": k.created_at,
            "updated_at": k.updated_at
        }
        for k in keywords
    ]


# 新增 /keyword/fetch-and-save 端點
@app.post("/keyword/fetch-and-save")
def fetch_and_save_keywords(db: Session = Depends(get_db)):
    """
    即時抓取 Google Trends 並寫入資料庫
    """
    keywords = fetch_daily_google_trends()
    repo = KeywordRepository(db)
    new_count = repo.batch_add(keywords)
    return {"message": "success", "count": new_count}

# # 1. 觸發文章生成（非同步）
@app.post("/articles")
def create_article(
    keyword_id: int = Body(...),
    is_highly_relevant: bool = Body(False),
    parameters: dict = Body(...),
    custom_prompt: str = Body(None),
):
    # 觸發 Celery 任務
    task = generate_article_task.delay(keyword_id, parameters, custom_prompt, is_highly_relevant)
    return {"message": "Article generation task has been accepted.", "task_id": task.id, "status": "pending_generation"}

# 2. 查詢待審核文章
@app.get("/articles")
def get_articles(status: str = "pending_review", db: Session = Depends(get_db)):
    repo = ArticleRepository(db)
    articles = repo.get_by_status(status)
    return [
        {
            "id": a.id,
            "title": a.title,
            "content": a.content,
            "keyword_id": a.keyword_id,
            "status": a.status,
            "created_at": a.created_at
        }
        for a in articles
    ]

# 3. 審核與更新文章內容
@app.patch("/articles/{article_id}")
def review_article(article_id: int, status: str = Body(...), content: str = Body(None), db: Session = Depends(get_db)):
    repo = ArticleRepository(db)
    article = repo.get_by_id(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    update_data = {"status": status}
    if content is not None:
        update_data["content"] = content
    repo.update(article_id, **update_data)
    return {"message": "Article has been updated.", "article_id": article_id, "status": status}