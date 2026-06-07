from __future__ import annotations

import asyncio
from contextlib import AbstractAsyncContextManager


class AsyncBulkhead(AbstractAsyncContextManager):
    def __init__(self, limit: int = 20) -> None:
        if limit < 1:
            raise ValueError("limit deve ser >= 1")
        self._semaphore = asyncio.Semaphore(limit)

    async def __aenter__(self):
        await self._semaphore.acquire()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self._semaphore.release()
        return False
