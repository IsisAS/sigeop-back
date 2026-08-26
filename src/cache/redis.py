import json
from typing import Any

import redis

from src.core.config import settings


class CacheService:
    def __init__(self):
        self.client = redis.from_url(settings.REDIS_SERVER, decode_responses=True)

    def get(self, key: str) -> Any:
        value = self.client.get(key)
        if value is None:
            return None
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value

    def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        serialized = json.dumps(value) if not isinstance(value, str) else value
        if ttl:
            self.client.setex(key, ttl, serialized)
        else:
            self.client.set(key, serialized)

    def delete(self, key: str) -> None:
        self.client.delete(key)

    def exists(self, key: str) -> bool:
        return self.client.exists(key) > 0

    def ttl(self, key: str) -> int:
        return self.client.ttl(key)
