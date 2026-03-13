from __future__ import annotations
import asyncio
from typing import Awaitable, Callable, TypeVar
T = TypeVar('T')

async def retry(operation: Callable[[], Awaitable[T]], *, attempts: int=3, base_delay_seconds: float=0.5) -> T:
    if attempts < 1:
        raise ValueError('attempts deve ser >= 1')
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return await operation()
        except Exception as exc:
            last_error = exc
            if attempt == attempts:
                break
            await asyncio.sleep(base_delay_seconds * attempt)
    assert last_error is not None
    raise last_error