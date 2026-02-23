"""Event bus port"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class EventBusPort(ABC):
    """Event bus interface"""

    @abstractmethod
    async def publish(self, event_type: str, payload: Dict[str, Any]) -> None:
        """Publish event to bus"""
        pass

    @abstractmethod
    async def subscribe(self, event_type: str, handler) -> None:
        """Subscribe to event"""
        pass
