"""Event bus port for cross-module decoupling."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class EventBusPort(ABC):
    """Minimal contract for publishing and subscribing to domain events."""

    @abstractmethod
    async def publish(self, event: Any) -> None:
        """Publish a domain event to the bus."""

    @abstractmethod
    def subscribe(self, event_name: str, handler: Any) -> None:
        """Register a handler for a given event name."""
