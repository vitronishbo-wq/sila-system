from __future__ import annotations

import asyncio
import time


class AsyncRateLimiter:
    """Simple token-bucket limiter for outbound integrations."""

    def __init__(self, *, rate: int = 100, per_seconds: float = 60.0) -> None:
        if rate < 1:
            raise ValueError("rate deve ser >= 1")
        if per_seconds <= 0:
            raise ValueError("per_seconds deve ser > 0")
        self._rate = float(rate)
        self._per_seconds = float(per_seconds)
        self._tokens = float(rate)
        self._updated_at = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        while True:
            async with self._lock:
                now = time.monotonic()
                elapsed = now - self._updated_at
                self._updated_at = now
                refill = elapsed / self._per_seconds * self._rate
                self._tokens = min(self._rate, self._tokens + refill)
                if self._tokens >= 1.0:
                    self._tokens -= 1.0
                    return
                deficit = 1.0 - self._tokens
                wait_seconds = max(deficit / self._rate * self._per_seconds, 0.001)
            await asyncio.sleep(wait_seconds)
