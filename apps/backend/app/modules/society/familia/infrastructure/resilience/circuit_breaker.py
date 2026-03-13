class CircuitBreaker:

    def __init__(self, failure_threshold: int=5) -> None:
        self.failure_threshold = failure_threshold
        self.failures = 0

    def record_failure(self) -> None:
        self.failures += 1

    def allow_request(self) -> bool:
        return self.failures < self.failure_threshold