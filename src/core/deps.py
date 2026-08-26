from src.cache.redis import CacheService
from src.db.session import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_cache():
    return CacheService()