"""Event bus assíncrono em memória para integração intercontexto."""
import asyncio
import logging
from datetime import datetime, timezone
from typing import Any, Callable
logger = logging.getLogger(__name__)

class _NoopAwaitable:
    """Permite `await bus.subscribe(...)` mantendo compatibilidade sync."""

    def __await__(self):
        if False:
            yield
        return None

class EventBus:

    def __init__(self):
        self._handlers: dict[str, list[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable):
        self._handlers.setdefault(event_type, []).append(handler)
        return _NoopAwaitable()

    async def publish(self, event_type: str, data: Any=None) -> dict[str, Any]:
        event = {
            'type': event_type,
            'data': data,
            'timestamp': datetime.now(timezone.utc).isoformat(),
        }
        for handler in self._handlers.get(event_type, []):
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as exc:
                logger.error('event.handler.error', extra={'error': str(exc), 'type': event_type})
        return event

class EventPublisher:
    """Facade legado compatível com assinaturas existentes."""
    _subscribers: dict[str, list[Callable]] = {}

    @classmethod
    def subscribe(cls, event_type: Any, handler: Callable):
        key = getattr(event_type, '__name__', str(event_type))
        cls._subscribers.setdefault(key, []).append(handler)

    @classmethod
    async def publish(cls, event: Any):
        event_type = getattr(event, '__class__', type(event)).__name__
        for handler in list(cls._subscribers.get(event_type, [])):
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as exc:
                logger.error('event.publisher.error', extra={'error': str(exc), 'type': event_type})
        return event
_event_bus = EventBus()
_event_store: list[dict[str, Any]] = []

def get_event_bus() -> EventBus:
    return _event_bus

def get_recent_events(limit: int=100) -> list[dict[str, Any]]:
    return _event_store[-limit:]

def get_events_by_type(event_type: str) -> list[dict[str, Any]]:
    return [e for e in _event_store if e.get('type') == event_type]

async def store_event(event: dict[str, Any]) -> None:
    _event_store.append(event)
    if len(_event_store) > 1000:
        _event_store.pop(0)
