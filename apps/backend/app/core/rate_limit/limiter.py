"""Simple in-memory token bucket limiter."""
import time
from collections import defaultdict

class RateLimitExceeded(Exception):
    """Raised when rate limit is exceeded."""

class InMemoryRateLimiter:

    def __init__(self, requests: int=60, per_seconds: int=60):
        self.requests = requests
        self.per_seconds = per_seconds
        self._buckets: dict[str, list[float]] = defaultdict(list)

    def check(self, key: str) -> bool:
        now = time.time()
        window_start = now - self.per_seconds
        bucket = self._buckets[key]
        bucket[:] = [t for t in bucket if t >= window_start]
        if len(bucket) >= self.requests:
            raise RateLimitExceeded(f"Rate limit exceeded for '{key}' ({self.requests}/{self.per_seconds}s)")
        bucket.append(now)
        return True