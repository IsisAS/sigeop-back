from fastapi import APIRouter, Depends

from src.cache.redis import CacheService
from src.integrations.ciclo.ciclo_client import CicloClient
from src.core.deps import get_cache

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/redis")
def redis_health(cache: CacheService = Depends(get_cache)):
    try:
        cache.client.ping()
        return {"status": "healthy", "service": "redis"}
    except Exception as e:
        return {"status": "unhealthy", "service": "redis", "detail": str(e)}

@router.get("/ciclo")
def ciclo_health():
    client = CicloClient()
    if client.health_check():
        return {"status": "healthy", "service": "ciclo"}
    return {"status": "unhealthy", "service": "ciclo", "detail": ""}