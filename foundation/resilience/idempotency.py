from __future__ import annotations

import asyncio
import json
import os
import time
from abc import ABC, abstractmethod
from collections.abc import Callable
from functools import wraps
from inspect import signature
from typing import Any, TypeVar

try:
    import redis.asyncio as redis_async
except ImportError:  # pragma: no cover
    redis_async = None

T = TypeVar("T")


class IdempotencyError(Exception):
    """Base exception for idempotency guard failures."""


class IdempotencyKeyMissingError(IdempotencyError):
    """Raised when an operation is attempted without an Idempotency-Key."""


class DuplicateRequestError(IdempotencyError):
    """Raised when the same idempotency key is reused for an already completed operation."""


class IdempotencyStore(ABC):
    """Abstract storage interface for idempotency keys."""

    @abstractmethod
    async def get(self, key: str) -> Any | None:
        ...

    @abstractmethod
    async def set(self, key: str, value: Any, ttl_seconds: int = 0) -> None:
        ...

    @abstractmethod
    async def exists(self, key: str) -> bool:
        ...

    @abstractmethod
    async def delete(self, key: str) -> None:
        ...


class RedisIdempotencyStore(IdempotencyStore):
    """Redis-backed idempotency store for production use."""

    def __init__(self, client: redis_async.Redis):
        if redis_async is None:
            raise RuntimeError("redis.asyncio is required for RedisIdempotencyStore")
        self._client = client

    @classmethod
    def from_url(
        cls,
        redis_url: str,
        decode_responses: bool = True,
        encoding: str = "utf-8",
        **kwargs: Any,
    ) -> RedisIdempotencyStore:
        if redis_async is None:
            raise RuntimeError("redis.asyncio is required for RedisIdempotencyStore")
        client = redis_async.from_url(
            redis_url,
            decode_responses=decode_responses,
            encoding=encoding,
            **kwargs,
        )
        return cls(client)

    async def get(self, key: str) -> Any | None:
        raw = await self._client.get(key)
        if raw is None:
            return None
        return json.loads(raw)

    async def set(self, key: str, value: Any, ttl_seconds: int = 0) -> None:
        payload = json.dumps(value, default=str)
        if ttl_seconds and ttl_seconds > 0:
            await self._client.setex(key, ttl_seconds, payload)
        else:
            await self._client.set(key, payload)

    async def exists(self, key: str) -> bool:
        return bool(await self._client.exists(key))

    async def delete(self, key: str) -> None:
        await self._client.delete(key)


class InMemoryIdempotencyStore(IdempotencyStore):
    """Lightweight in-memory store for idempotency keys and completion markers."""

    def __init__(self) -> None:
        self._store: dict[str, tuple[float, Any]] = {}
        self._lock = asyncio.Lock()

    async def _prune(self) -> None:
        now = time.time()
        expired_keys = [key for key, (expiry, _) in self._store.items() if expiry and expiry <= now]
        for key in expired_keys:
            self._store.pop(key, None)

    async def get(self, key: str) -> Any | None:
        async with self._lock:
            await self._prune()
            entry = self._store.get(key)
            return entry[1] if entry else None

    async def set(self, key: str, value: Any, ttl_seconds: int = 0) -> None:
        expiry = time.time() + ttl_seconds if ttl_seconds > 0 else 0.0
        async with self._lock:
            await self._prune()
            self._store[key] = (expiry, value)

    async def exists(self, key: str) -> bool:
        async with self._lock:
            await self._prune()
            return key in self._store

    async def delete(self, key: str) -> None:
        async with self._lock:
            self._store.pop(key, None)


_default_store = InMemoryIdempotencyStore()


def normalize_idempotency_key(value: str | None) -> str:
    if not value or not value.strip():
        raise IdempotencyKeyMissingError("Idempotency-Key header is required for critical operations.")
    return value.strip()


def extract_idempotency_key(headers: dict[str, str] | None) -> str | None:
    if not headers:
        return None
    for header_name in ("Idempotency-Key", "idempotency-key", "idemPotency-key"):
        if header_name in headers:
            return normalize_idempotency_key(headers[header_name])
    return None


def create_redis_idempotency_store(redis_url: str | None = None) -> RedisIdempotencyStore:
    """Create a RedisIdempotencyStore using an environment-provided REDIS_URL."""
    if redis_url is None:
        redis_url = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
    return RedisIdempotencyStore.from_url(redis_url)


def _resolve_idempotency_key(func: Callable[..., Any], args: tuple[Any, ...], kwargs: dict[str, Any]) -> str:
    sig = signature(func)
    bound = sig.bind_partial(*args, **kwargs)
    return normalize_idempotency_key(bound.arguments.get("idempotency_key"))


def _make_store_key(operation_name: str, idempotency_key: str) -> str:
    return f"idempotency:{operation_name}:{idempotency_key}"


def idempotent(
    operation_name: str | None = None,
    store: IdempotencyStore | None = None,
    ttl_seconds: int = 3600,
) -> Callable[[Callable[..., T]], Callable[..., T | Awaitable[T]]]:
    """Decorator to protect critical operations with an Idempotency-Key."""

    def decorator(func: Callable[..., T]) -> Callable[..., T | Awaitable[T]]:
        resolved_name = operation_name or f"{func.__module__}.{func.__qualname__}"
        chosen_store = store or _default_store

        def _get_key(args: tuple[Any, ...], kwargs: dict[str, Any]) -> str:
            return _make_store_key(resolved_name, _resolve_idempotency_key(func, args, kwargs))

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> T:
            key = _get_key(args, kwargs)
            if await chosen_store.exists(key):
                value = await chosen_store.get(key)
                if isinstance(value, dict) and value.get("completed"):
                    raise DuplicateRequestError("Duplicate request detected for idempotency key.")
                raise DuplicateRequestError("Duplicate request in progress or already completed.")

            await chosen_store.set(key, {"completed": False}, ttl_seconds)
            try:
                result = await func(*args, **kwargs)
                await chosen_store.set(key, {"completed": True, "result": result}, ttl_seconds)
                return result
            except Exception:
                await chosen_store.delete(key)
                raise

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> T:
            key = _get_key(args, kwargs)
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None

            if loop is not None and loop.is_running():
                raise RuntimeError("Sync idempotent decorator cannot run inside an active event loop")

            async def _run() -> T:
                if await chosen_store.exists(key):
                    value = await chosen_store.get(key)
                    if isinstance(value, dict) and value.get("completed"):
                        raise DuplicateRequestError("Duplicate request detected for idempotency key.")
                    raise DuplicateRequestError("Duplicate request in progress or already completed.")
                await chosen_store.set(key, {"completed": False}, ttl_seconds)
                try:
                    result = func(*args, **kwargs)
                    await chosen_store.set(key, {"completed": True, "result": result}, ttl_seconds)
                    return result
                except Exception:
                    await chosen_store.delete(key)
                    raise

            return asyncio.new_event_loop().run_until_complete(_run())

        if asyncio.iscoroutinefunction(func):
            return async_wrapper  # type: ignore[return-value]
        return sync_wrapper  # type: ignore[return-value]

    return decorator
