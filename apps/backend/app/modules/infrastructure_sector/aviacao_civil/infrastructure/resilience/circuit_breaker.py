from __future__ import annotations
import asyncio
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import wraps
from typing import Any

@dataclass
class _State:
    failures: int = 0
    opened_until: datetime | None = None

class CircuitOpenError(RuntimeError):
    pass
_STATES: dict[str, _State] = {}
_LOCK = asyncio.Lock()

def circuit_breaker(name: str, failure_threshold: int=3, recovery_timeout: int=60) -> Callable:

    def decorator(fn: Callable) -> Callable:

        @wraps(fn)
        async def wrapper(*args: Any, **kwargs: Any):
            async with _LOCK:
                state = _STATES.setdefault(name, _State())
                if state.opened_until and datetime.utcnow() < state.opened_until:
                    raise CircuitOpenError(f'Circuito {name} aberto')
            try:
                result = await fn(*args, **kwargs)
            except Exception:
                async with _LOCK:
                    state = _STATES.setdefault(name, _State())
                    state.failures += 1
                    if state.failures >= failure_threshold:
                        state.opened_until = datetime.utcnow() + timedelta(seconds=recovery_timeout)
                raise
            async with _LOCK:
                state = _STATES.setdefault(name, _State())
                state.failures = 0
                state.opened_until = None
            return result
        return wrapper
    return decorator