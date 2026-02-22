from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional
from datetime import datetime


class DomainEvent:
    """Base para eventos de domínio"""
    event_version: int = 1
    event_type: str
    
    def __init__(self, **kwargs):
        self.timestamp = datetime.now()
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            k: v.isoformat() if isinstance(v, datetime) else v
            for k, v in self.__dict__.items()
        }


class EventBusPort(ABC):
    """Interface para bus de eventos de domínio"""
    
    @abstractmethod
    async def publish(self, event: DomainEvent) -> None:
        """Publica um evento de domínio"""
        pass
    
    @abstractmethod
    async def publish_all(self, events: List[DomainEvent]) -> None:
        """Publica múltiplos eventos"""
        pass
    
    @abstractmethod
    def subscribe(self, event_type: str, handler: Callable):
        """Subscreve a um tipo de evento"""
        pass
    
    @abstractmethod
    async def unsubscribe(self, event_type: str, handler: Callable) -> None:
        """Desinscreve de um tipo de evento"""
        pass
