"""Async lock manager baseline (swapable for Redis/Postgres locks)."""

import asyncio


class LockManager:
    def __init__(self):
        self._locks: dict[str, asyncio.Lock] = {}

    def _get_lock(self, key: str) -> asyncio.Lock:
        if key not in self._locks:
            self._locks[key] = asyncio.Lock()
        return self._locks[key]

    async def acquire(self, key: str):
        lock = self._get_lock(key)
        await lock.acquire()
        return lock

    async def release(self, key: str) -> None:
        lock = self._locks.get(key)
        if lock and lock.locked():
            lock.release()
