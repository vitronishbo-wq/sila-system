from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Optional

try:
    import redis.asyncio as redis_async
except Exception:
    redis_async = None


class SLAEngineCache:
    def __init__(self, url: str | None = None, ttl_seconds: int = 300):
        self._ttl = ttl_seconds
        self._memory: Dict[str, Any] = {}
        self._redis = None
        if redis_async and url:
            self._redis = redis_async.from_url(url, decode_responses=True)

    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        if self._redis:
            raw = await self._redis.get(key)
            if raw:
                return json.loads(raw)
        return self._memory.get(key)

    async def set(self, key: str, value: Dict[str, Any]) -> None:
        if self._redis:
            await self._redis.set(key, json.dumps(value), ex=self._ttl)
            return
        self._memory[key] = value


class SLACache:
    """
    Cache Redis para resultados de SLA
    Reduz carga no banco e acelera respostas
    """

    def __init__(self, redis_client: Any | None = None, ttl: int = 300):
        self._redis = redis_client
        self._ttl = ttl
        self._prefix = "sla:calc:"
        self._memory: Dict[str, Any] = {}

    def _generate_key(self, service_id: str, context: Optional[Dict] = None) -> str:
        if context:
            context_str = json.dumps(context, sort_keys=True)
            context_hash = hashlib.md5(context_str.encode()).hexdigest()[:8]
            return f"{self._prefix}{service_id}:{context_hash}"
        return f"{self._prefix}{service_id}"

    async def get(self, service_id: str, context: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        key = self._generate_key(service_id, context)
        if self._redis:
            raw = await self._redis.get(key)
            if raw:
                return json.loads(raw)
        return self._memory.get(key)

    async def set(
        self,
        service_id: str,
        context: Optional[Dict],
        value: Dict[str, Any],
        ttl: Optional[int] = None,
    ) -> None:
        key = self._generate_key(service_id, context)
        if self._redis:
            await self._redis.setex(key, ttl or self._ttl, json.dumps(value, default=str))
            return
        self._memory[key] = value

    async def invalidate(self, service_id: str) -> None:
        pattern = f"{self._prefix}{service_id}:*"
        if self._redis:
            async for key in self._redis.scan_iter(match=pattern):
                await self._redis.delete(key)
        else:
            for key in list(self._memory.keys()):
                if key.startswith(f"{self._prefix}{service_id}:"):
                    self._memory.pop(key, None)

    async def invalidate_all(self) -> None:
        pattern = f"{self._prefix}*"
        if self._redis:
            async for key in self._redis.scan_iter(match=pattern):
                await self._redis.delete(key)
        else:
            self._memory.clear()
