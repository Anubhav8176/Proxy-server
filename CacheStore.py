from dataclasses import dataclass, field
import time


@dataclass
class CacheData:
    status: int
    headers: dict = field(default_factory=dict)
    body: bytes
    created_at: float = field(default_factory=time.time)

    def is_expired(self, ttl: int = 60)->bool:
        return (time.time() - self.created_at) > ttl
    

class CacheStore:
    def __init__(self):
        self._store: dict[str, CacheData] = {}

    def get(self, key: str) -> CacheData | None:
        entry = self._store.get(key)
        if entry is None or entry.is_expired():
            return None
        return entry
    
    def clear(self):
        self._store.clear()
        print("Cache cleared!")

    def set(self, key: str, status: int, body: bytes, headers: dict):
        self._store[key] = CacheData(
            status=status,
            headers=headers,
            body=body
        )