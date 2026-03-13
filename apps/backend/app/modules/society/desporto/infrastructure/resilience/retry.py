from __future__ import annotations
import asyncio
from collections.abc import Callable
from functools import wraps
from typing import Any

def with_retry(attempts: int=3, backoff_seconds: float=0.5) -> Callable:

    def decorator(fn: Callable) -> Callable:

        @wraps(fn)
        async def wrapper(*args: Any, **kwargs: Any):
            last_error: Exception | None = None
            for idx in range(attempts):
                try:
                    return await fn(*args, **kwargs)
                except Exception as exc:
                    last_error = exc
                    if idx == attempts - 1:
                        break
                    await asyncio.sleep(backoff_seconds * (idx + 1))
            if last_error is not None:
                raise last_error
            return None
        return wrapper
    return decorator