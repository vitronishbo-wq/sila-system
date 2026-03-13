import asyncio
import inspect
from functools import wraps
from .policy import FailurePolicy
from .registry import CircuitRegistry

def circuit_breaker(name: str | None=None, failure_threshold: int=5, recovery_timeout: float=30.0, success_threshold: int=3):
    """Decorator to execute async operations behind a named circuit breaker."""
    policy = FailurePolicy(failure_threshold=failure_threshold, recovery_timeout=recovery_timeout, success_threshold=success_threshold)

    def wrapper(func):
        circuit_name = name or f'{func.__module__}.{func.__qualname__}'
        circuit = CircuitRegistry.get(circuit_name, policy=policy)

        @wraps(func)
        async def inner(*args, **kwargs):
            return await circuit.call(func, *args, **kwargs)
        if inspect.iscoroutinefunction(func):
            return inner

        @wraps(func)
        def inner_sync(*args, **kwargs):
            try:
                asyncio.get_running_loop()
            except RuntimeError:
                return asyncio.run(circuit.call(func, *args, **kwargs))
            raise RuntimeError('Sync function decorated with circuit_breaker called inside a running event loop')
        return inner_sync
    return wrapper

def with_circuit_breaker(name: str | None=None, failure_threshold: int=5, recovery_timeout: float=30.0, success_threshold: int=3):
    """Compatibility alias for previous decorator name."""
    return circuit_breaker(name=name, failure_threshold=failure_threshold, recovery_timeout=recovery_timeout, success_threshold=success_threshold)

def with_retry(max_retries: int=3, base_delay: float=0.5, max_delay: float=30.0):
    """Retry decorator with exponential backoff for async callables."""
    if max_retries <= 0:
        raise ValueError('max_retries must be > 0')

    def wrapper(func):

        @wraps(func)
        async def inner(*args, **kwargs):
            last_error: Exception | None = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as exc:
                    last_error = exc
                    if attempt == max_retries - 1:
                        break
                    delay = min(base_delay * 2 ** attempt, max_delay)
                    await asyncio.sleep(delay)
            raise last_error or RuntimeError('retry failed')
        if inspect.iscoroutinefunction(func):
            return inner

        @wraps(func)
        def inner_sync(*args, **kwargs):
            last_error: Exception | None = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_error = exc
                    if attempt == max_retries - 1:
                        break
                    delay = min(base_delay * 2 ** attempt, max_delay)
                    asyncio.run(asyncio.sleep(delay))
            raise last_error or RuntimeError('retry failed')
        return inner_sync
    return wrapper

def with_timeout(seconds: float):
    """Timeout decorator for async callables."""
    if seconds <= 0:
        raise ValueError('seconds must be > 0')

    def wrapper(func):

        @wraps(func)
        async def inner(*args, **kwargs):
            return await asyncio.wait_for(func(*args, **kwargs), timeout=seconds)
        if inspect.iscoroutinefunction(func):
            return inner

        @wraps(func)
        def inner_sync(*args, **kwargs):
            try:
                asyncio.get_running_loop()
            except RuntimeError:
                return asyncio.run(asyncio.wait_for(asyncio.to_thread(func, *args, **kwargs), timeout=seconds))
            raise RuntimeError('Sync function decorated with with_timeout called inside a running event loop')
        return inner_sync
    return wrapper