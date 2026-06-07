"""Adapter that binds the core EventBus implementation to the EventBusPort."""

from __future__ import annotations

from typing import Any

from apps.backend.app.core.events.bus_enhanced import EventBus as EnhancedEventBus
from apps.backend.app.core.events.models import DomainEvent
from apps.backend.app.core.events.ports import EventBusPort
from apps.backend.app.core.events.registry import HandlerRegistry


class EventBusAdapter(EventBusPort):
    """Event bus adapter using the enhanced core EventBus."""

    async def publish(self, event: Any) -> None:
        await EnhancedEventBus.publish(self._coerce_event(event))

    def subscribe(self, event_name: str | type, handler: Any) -> None:
        if isinstance(event_name, str):
            name = event_name
        else:
            name = getattr(event_name, "event_name", None) or getattr(
                event_name, "__name__", str(event_name)
            )
        HandlerRegistry.register(name, handler)

    @staticmethod
    def _coerce_event(event: Any) -> DomainEvent:
        if isinstance(event, DomainEvent):
            return event
        name = (
            getattr(event, "name", None)
            or getattr(event, "event_name", None)
            or getattr(event, "__class__", type(event)).__name__
        )
        payload = None
        if hasattr(event, "payload"):
            payload = event.payload
        elif hasattr(event, "to_payload"):
            try:
                payload = event.to_payload()
            except Exception:
                payload = None
        if payload is None:
            payload = dict(getattr(event, "__dict__", {}))
        metadata = getattr(event, "metadata", None) or {}
        occurred_at = getattr(event, "occurred_at", None)
        if occurred_at is not None:
            return DomainEvent(
                name=name, payload=payload, occurred_at=occurred_at, metadata=metadata
            )
        return DomainEvent(name=name, payload=payload, metadata=metadata)
