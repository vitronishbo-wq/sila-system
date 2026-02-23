"""Core events - EventBus"""
import asyncio
import json
import logging
from typing import Dict, Any, Callable, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class EventBus:
    """Event Bus em memória"""
    
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
    
    async def publish(self, event_type: str, data: Any = None):
        event = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(event)
                    else:
                        handler(event)
                except Exception as e:
                    logger.error(f"Handler error: {e}")
        
        return event

_event_bus = EventBus()
_event_store: List[Dict[str, Any]] = []  # Store for recent events

def get_event_bus() -> EventBus:
    """Get singleton EventBus"""
    return _event_bus

def get_recent_events(limit: int = 100) -> list:
    """Get recent events from store"""
    return _event_store[-limit:]

def get_events_by_type(event_type: str) -> list:
    """Filter events by type"""
    return [e for e in _event_store if e.get("type") == event_type]

async def store_event(event: Dict[str, Any]):
    """Store event in memory"""
    _event_store.append(event)
    if len(_event_store) > 1000:  # Keep only last 1000
        _event_store.pop(0)

def get_event_bus() -> EventBus:
    return _event_bus

__all__ = [
    'EventBus', 'get_event_bus', 'get_recent_events', 
    'get_events_by_type', 'store_event'
]
