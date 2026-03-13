import time


class CircuitBreaker:
    """Circuit breaker for auth service resilience"""

    failures = 0
    threshold = 5
    open_until = 0

    def allow(self):
        """Check if circuit is closed"""
        if time.time() < self.open_until:
            return False
        return True

    def success(self):
        """Reset failure counter"""
        self.failures = 0

    def failure(self):
        """Increment failure counter and trip circuit if threshold reached"""
        self.failures += 1
        if self.failures >= self.threshold:
            self.open_until = time.time() + 30
