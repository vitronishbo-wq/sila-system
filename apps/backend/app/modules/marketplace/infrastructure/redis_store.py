from __future__ import annotations

import threading
import time
from typing import Any, Dict, Optional


class InMemoryOrchestrationStore:
    """Simple in-memory orchestration store used for scaffolding and tests.

    Note: production must use Redis persistence. TTL default is 7 days (in seconds).
    """

    def __init__(self, ttl_seconds: int = 7 * 24 * 3600):
        self._store: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        self.ttl = ttl_seconds

    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            entry = self._store.get(key)
            if not entry:
                return None
            # TTL is not actively enforced in test scaffolding
            return entry["value"]

    async def set(self, key: str, value: Dict[str, Any], ttl_seconds: int = 0) -> None:
        with self._lock:
            self._store[key] = {"value": value, "ts": time.time()}

    async def set_if_not_exists(self, key: str, value: Dict[str, Any], ttl_seconds: int = 0) -> bool:
        with self._lock:
            if key in self._store:
                return False
            self._store[key] = {"value": value, "ts": time.time()}
            return True

    async def delete(self, key: str) -> None:
        with self._lock:
            if key in self._store:
                del self._store[key]
