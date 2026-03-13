import inspect
import logging
import threading
import time
from collections.abc import Callable
from typing import Any, TypeVar
from .exceptions import CircuitBreakerOpen
from .policy import FailurePolicy
from .state import CircuitState
T = TypeVar('T')
logger = logging.getLogger('sila.core.resilience')

class CircuitBreaker:
    """Async-ready circuit breaker with closed/open/half-open states."""

    def __init__(self, name: str, policy: FailurePolicy | None=None):
        self.name = name
        self.policy = policy or FailurePolicy()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: float | None = None
        self._lock = threading.RLock()

    async def call(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> T:
        self._check_state()
        try:
            result = func(*args, **kwargs)
            if inspect.isawaitable(result):
                result = await result
        except Exception as exc:
            self._on_failure(exc)
            raise
        self._on_success()
        return result

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return {'name': self.name, 'state': self.state.value, 'failure_count': self.failure_count, 'success_count': self.success_count, 'last_failure_time': self.last_failure_time, 'policy': {'failure_threshold': self.policy.failure_threshold, 'recovery_timeout': self.policy.recovery_timeout, 'success_threshold': self.policy.success_threshold}}

    def _check_state(self) -> None:
        with self._lock:
            if self.state != CircuitState.OPEN:
                return
            now = time.time()
            if self.last_failure_time is None:
                self.last_failure_time = now
            elapsed = now - self.last_failure_time
            if elapsed >= self.policy.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
                logger.info('circuit.half_open', extra={'circuit': self.name})
                return
            raise CircuitBreakerOpen(circuit=self.name, retry_after=max(0.0, self.policy.recovery_timeout - elapsed))

    def _on_failure(self, exc: Exception) -> None:
        with self._lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            logger.error('circuit.failure', extra={'circuit': self.name, 'state': self.state.value, 'failures': self.failure_count, 'error': type(exc).__name__})
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.OPEN
                self.success_count = 0
                logger.error('circuit.reopened', extra={'circuit': self.name})
                return
            if self.failure_count >= self.policy.failure_threshold:
                self.state = CircuitState.OPEN
                self.success_count = 0
                logger.error('circuit.opened', extra={'circuit': self.name})

    def _on_success(self) -> None:
        with self._lock:
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.policy.success_threshold:
                    self._reset()
                return
            self.failure_count = 0

    def _reset(self) -> None:
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        logger.info('circuit.closed', extra={'circuit': self.name})