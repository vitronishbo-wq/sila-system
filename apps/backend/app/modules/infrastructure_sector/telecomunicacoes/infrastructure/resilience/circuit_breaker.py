from __future__ import annotations
import time
from functools import wraps

class CircuitBreaker:

    def __init__(self, *, failure_threshold: int=3, recovery_timeout: int=30) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time: float | None = None
        self.state = 'CLOSED'

    def __call__(self, func):

        @wraps(func)
        async def wrapper(*args, **kwargs):
            if self.state == 'OPEN':
                now = time.time()
                if self.last_failure_time is None or now - self.last_failure_time <= self.recovery_timeout:
                    raise RuntimeError('Circuit OPEN')
                self.state = 'HALF_OPEN'
            try:
                result = await func(*args, **kwargs)
                self.failures = 0
                self.state = 'CLOSED'
                return result
            except Exception:
                self.failures += 1
                self.last_failure_time = time.time()
                if self.failures >= self.failure_threshold:
                    self.state = 'OPEN'
                raise
        return wrapper