from sqlalchemy.orm import declarative_base
Base = declarative_base()

# 統一 metadata 給 Alembic 用

# 這裡註冊所有 model，供 Alembic 自動偵測
__all__ = [
    "Base"
]
