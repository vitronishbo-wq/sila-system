from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from functools import wraps


class CircuitManager:
    _failures: dict[str, int] = defaultdict(int)
    _open_circuits: set[str] = set()
    _failure_threshold = 3

    @classmethod
    def is_open(cls, name: str) -> bool:
        return name in cls._open_circuits

    @classmethod
    def report_failure(cls, name: str) -> None:
        cls._failures[name] += 1
        if cls._failures[name] >= cls._failure_threshold:
            cls._open_circuits.add(name)

    @classmethod
    def report_success(cls, name: str) -> None:
        cls._failures[name] = 0
        cls._open_circuits.discard(name)

    @classmethod
    def reset(cls, name: str) -> None:
        cls._failures[name] = 0
        cls._open_circuits.discard(name)


def circuit_breaker(name: str) -> Callable:

    def decorator(func: Callable) -> Callable:

        @wraps(func)
        async def wrapper(*args, **kwargs):
            if CircuitManager.is_open(name):
                raise RuntimeError(f"Service {name} unavailable")
            try:
                result = await func(*args, **kwargs)
            except Exception:
                CircuitManager.report_failure(name)
                raise
            CircuitManager.report_success(name)
            return result

        return wrapper

    return decorator
