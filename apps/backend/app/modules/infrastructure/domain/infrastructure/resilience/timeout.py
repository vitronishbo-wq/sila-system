from __future__ import annotations
import asyncio
from typing import Awaitable, TypeVar
T = TypeVar('T')

async def with_timeout(operation: Awaitable[T], *, timeout_seconds: float=5.0) -> T:
    if timeout_seconds <= 0:
        raise ValueError('timeout_seconds deve ser > 0')
    return await asyncio.wait_for(operation, timeout=timeout_seconds)