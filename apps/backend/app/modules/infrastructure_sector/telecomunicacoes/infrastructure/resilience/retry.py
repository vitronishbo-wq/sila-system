from __future__ import annotations
import asyncio
from collections.abc import Callable

async def retry_async(func: Callable, *args, retries: int=3, delay_seconds: float=0.2, **kwargs):
    last_error = None
    for attempt in range(retries):
        try:
            return await func(*args, **kwargs)
        except Exception as exc:
            last_error = exc
            if attempt + 1 < retries:
                await asyncio.sleep(delay_seconds)
    raise last_error