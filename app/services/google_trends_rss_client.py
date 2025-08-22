import requests
import xml.etree.ElementTree as ET
import logging

from app.models.keyword import Keyword
from app.core.db import get_db
from sqlalchemy.orm import Session
from datetime import datetime

def fetch_daily_google_trends():
    url = "https://trends.google.com/trending/rss?geo=TW"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"[GoogleTrends] HTTP 請求失敗: {e}")
        return []
    try:
        root = ET.fromstring(resp.content)
        items = root.findall(".//item")
    except ET.ParseError as e:
        logging.error(f"[GoogleTrends] XML 解析失敗: {e}")
        return []
    keywords = []
    for idx, item in enumerate(items):
        try:
            title = item.findtext("title")
            raw_data = ET.tostring(item, encoding="unicode")
            keywords.append({
                "source": "Google Trends",
                "title": title,
                "url": item.findtext("link"),
                # 暫時不使用
                # "hotness_score": idx + 1,
                "status": "pending_selection",
                "raw_data": raw_data
            })
        except Exception as e:
            logging.warning(f"[GoogleTrends] 單一 item 解析失敗: {e}")
    return keywords


def save_keywords_to_db(db: Session, keywords: list):
    """
    將關鍵字資料批次寫入資料庫
    """
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    # 取得今天已存在的 title set
    existing_titles = set(
        row[0] for row in db.query(Keyword.title)
        .filter(Keyword.fetched_at >= today_start, Keyword.fetched_at <= today_end)
        .all()
    )
    new_count = 0
    for kw in keywords:
        if kw["title"] in existing_titles:
            continue
        db.add(Keyword(
            source=kw["source"],
            title=kw["title"],
            url=kw["url"],
            # 暫時不使用
            # hotness_score=kw["hotness_score"],
            status=kw["status"],
            raw_data=kw["raw_data"],
            fetched_at=now
        ))
        existing_titles.add(kw["title"])
        new_count += 1
    db.commit()
    return new_count
