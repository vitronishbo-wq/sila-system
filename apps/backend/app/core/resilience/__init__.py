"""Core resilience primitives for fault tolerance."""

from .circuit_breaker import CircuitBreaker
from .config import ResilienceConfig, build_policy
from .decorators import circuit_breaker, with_circuit_breaker, with_retry, with_timeout
from .exceptions import CircuitBreakerError, CircuitBreakerOpen
from .policy import FailurePolicy
from .registry import CircuitRegistry
from .state import CircuitState

try:
    from .http_client import ResilientClient
except Exception:
    ResilientClient = None
__all__ = [
    "CircuitBreaker",
    "CircuitBreakerError",
    "CircuitBreakerOpen",
    "CircuitRegistry",
    "CircuitState",
    "FailurePolicy",
    "ResilienceConfig",
    "ResilientClient",
    "build_policy",
    "circuit_breaker",
    "with_circuit_breaker",
    "with_retry",
    "with_timeout",
]
