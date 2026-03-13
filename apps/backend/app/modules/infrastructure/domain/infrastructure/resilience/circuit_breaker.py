from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

@dataclass
class CircuitBreaker:
    failure_threshold: int = 5
    reset_timeout_seconds: int = 30
    _failures: int = 0
    _opened_at: datetime | None = field(default=None, init=False)

    def is_open(self) -> bool:
        if self._opened_at is None:
            return False
        if datetime.now(timezone.utc) - self._opened_at >= timedelta(seconds=self.reset_timeout_seconds):
            self._opened_at = None
            self._failures = 0
            return False
        return True

    def record_success(self) -> None:
        self._failures = 0
        self._opened_at = None

    def record_failure(self) -> None:
        self._failures += 1
        if self._failures >= self.failure_threshold:
            self._opened_at = datetime.now(timezone.utc)