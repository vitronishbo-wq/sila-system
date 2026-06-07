from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

try:
    import redis.asyncio as redis_async
except ImportError:  # pragma: no cover
    redis_async = None


class RedisOrchestrationStore:
    """Redis-backed orchestration store using JSON serialization."""

    def __init__(self, client: "redis_async.Redis"):
        if redis_async is None:
            raise RuntimeError("redis.asyncio is required for RedisOrchestrationStore")
        self._client = client

    @classmethod
    def from_url(cls, redis_url: str | None = None, **kwargs: Any) -> "RedisOrchestrationStore":
        if redis_async is None:
            raise RuntimeError("redis.asyncio is required for RedisOrchestrationStore")
        if redis_url is None:
            redis_url = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
        client = redis_async.from_url(redis_url, decode_responses=True, **kwargs)
        return cls(client)

    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        raw = await self._client.get(key)
        if raw is None:
            return None
        return json.loads(raw)

    async def set(self, key: str, value: Dict[str, Any], ttl_seconds: int = 0) -> None:
        payload = json.dumps(value, default=str)
        if ttl_seconds and ttl_seconds > 0:
            await self._client.setex(key, ttl_seconds, payload)
        else:
            await self._client.set(key, payload)

    async def set_if_not_exists(self, key: str, value: Dict[str, Any], ttl_seconds: int = 0) -> bool:
        payload = json.dumps(value, default=str)
        # Use SET NX with EX if ttl provided
        if ttl_seconds and ttl_seconds > 0:
            return await self._client.set(key, payload, nx=True, ex=ttl_seconds)
        return await self._client.set(key, payload, nx=True)

    async def delete(self, key: str) -> None:
        await self._client.delete(key)
