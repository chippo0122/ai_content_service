from celery import Celery
from app.services.google_trends_rss_client import fetch_daily_google_trends, save_keywords_to_db
from app.core.db import SessionLocal
from app.services.article_generation_service import ArticleGenerationService

import os
from dotenv import load_dotenv
load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_DB = os.getenv("REDIS_DB", "0")
# REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

# 若有密碼，格式為 redis://:password@host:port/db
# broker_url = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

celery_app = Celery(
    "ai_content_service",
    broker=broker_url,
    backend=broker_url
)

celery_app.conf.beat_schedule = {
    'fetch-and-save-keywords-every-hour': {
        'task': 'app.core.celery_worker.fetch_and_save_keywords_task',
        'schedule': 3600.0,  # 每3600秒（1小時）執行一次
    },
}

@celery_app.task
def generate_article_task(keyword_id, parameters, custom_prompt=None, is_highly_relevant=False):
    db = SessionLocal()
    try:
        service = ArticleGenerationService(db)
        service.generate_article(keyword_id, parameters, custom_prompt, is_highly_relevant)
    finally:
        db.close()

@celery_app.task
def fetch_and_save_keywords_task():
    db = SessionLocal()
    try:
        keywords = fetch_daily_google_trends()
        save_keywords_to_db(db, keywords)
    finally:
        db.close()
