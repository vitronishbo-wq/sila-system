class CircuitBreakerOpen(Exception):
    """Raised when circuit is open and calls are blocked."""

    def __init__(self, circuit: str, retry_after: float | None=None):
        self.circuit = circuit
        self.retry_after = retry_after
        msg = f"Circuit '{circuit}' is open"
        if retry_after is not None:
            msg = f'{msg}; retry after {retry_after:.2f}s'
        super().__init__(msg)

class CircuitBreakerError(Exception):
    """Raised when circuit breaker fails internally."""