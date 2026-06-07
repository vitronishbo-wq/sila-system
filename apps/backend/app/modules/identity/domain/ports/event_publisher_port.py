from abc import ABC, abstractmethod
from typing import Any


class EventPublisherPort(ABC):
    """Port: Domain event publishing interface."""

    @abstractmethod
    async def publish(self, event_name: str, event_data: dict[str, Any]) -> None:
        pass

    @abstractmethod
    async def subscribe(self, event_name: str, handler) -> None:
        pass

    @abstractmethod
    async def unsubscribe(self, event_name: str, handler) -> None:
        pass
