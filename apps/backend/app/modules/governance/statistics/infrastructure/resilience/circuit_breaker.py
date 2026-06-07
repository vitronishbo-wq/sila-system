from __future__ import annotations


class CircuitBreaker:
    def __init__(self, threshold: int = 5) -> None:
        self.threshold = threshold
        self.failures = 0
        self.open = False

    def mark_success(self) -> None:
        self.failures = 0
        self.open = False

    def mark_failure(self) -> None:
        self.failures += 1
        if self.failures >= self.threshold:
            self.open = True

    def can_execute(self) -> bool:
        return not self.open
