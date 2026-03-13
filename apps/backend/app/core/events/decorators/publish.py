"""Decorators for automatic event publishing."""
from functools import wraps
from typing import Callable, Any
from app.core.observability.enterprise_logging import get_logger
logger = get_logger('core.events.decorators')

def publish_event(event_factory: Callable) -> Callable:
    """Decorator to automatically publish events after function execution.
    
    Usage:
        ```python
        @publish_event(UserLoggedIn)
        async def handle_login(username: str) -> User:
            user = authenticate(username)
            return user  # Result passed to event_factory
        ```
    
    The decorated function's result is passed to event_factory which should
    return a DomainEvent instance.
    
    Args:
        event_factory: Callable that receives function result and returns DomainEvent
        
    Returns:
        Decorated function that publishes event after execution
    """

    def decorator(func: Callable) -> Callable:

        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            """Async wrapper for automatic event publishing."""
            result = await func(*args, **kwargs)
            try:
                event = event_factory(result)
                from .bus import EventBus
                await EventBus.publish(event)
                logger.debug('event_published_via_decorator', extra={'event': event.name, 'function': func.__name__})
            except Exception as e:
                logger.error('decorator_event_publish_failed', extra={'error': str(e), 'function': func.__name__})
            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            """Sync wrapper (not recommended for event-driven code)."""
            logger.warning('publish_event_decorator_on_sync_function', extra={'function': func.__name__})
            result = func(*args, **kwargs)
            return result
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    return decorator
import asyncio