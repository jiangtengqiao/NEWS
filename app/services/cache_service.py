from cachetools import TTLCache
from typing import Optional, Any


class CacheService:
    def __init__(self, maxsize: int = 1000, ttl: int = 300):
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl)

    def get(self, key: str) -> Optional[Any]:
        return self.cache.get(key)

    def set(self, key: str, value: Any) -> None:
        self.cache[key] = value

    def delete(self, key: str) -> None:
        if key in self.cache:
            del self.cache[key]


cache_service = CacheService()
