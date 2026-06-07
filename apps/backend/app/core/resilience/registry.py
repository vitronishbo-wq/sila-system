import threading
from collections.abc import Mapping

from .circuit_breaker import CircuitBreaker
from .policy import FailurePolicy


class CircuitRegistry:
    """Global registry to avoid duplicate circuit instances."""

    _circuits: dict[str, CircuitBreaker] = {}
    _lock = threading.RLock()

    @classmethod
    def get(cls, name: str, policy: FailurePolicy | None = None) -> CircuitBreaker:
        with cls._lock:
            circuit = cls._circuits.get(name)
            if circuit is None:
                circuit = CircuitBreaker(name=name, policy=policy or FailurePolicy())
                cls._circuits[name] = circuit
            return circuit

    @classmethod
    def clear(cls) -> None:
        with cls._lock:
            cls._circuits.clear()

    @classmethod
    def snapshot(cls) -> Mapping[str, dict]:
        with cls._lock:
            return {name: cb.snapshot() for name, cb in cls._circuits.items()}
