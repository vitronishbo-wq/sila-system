"""Event bus port"""

from abc import ABC, abstractmethod
from typing import Any


class EventBusPort(ABC):
    """Event bus interface"""

    @abstractmethod
    async def publish(self, event_type: str, payload: dict[str, Any]) -> None:
        """Publish event to bus"""
        pass

    @abstractmethod
    async def subscribe(self, event_type: str, handler) -> None:
        """Subscribe to event"""
        pass
