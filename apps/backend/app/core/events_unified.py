"""Core Events - Universal Event Bus"""
import asyncio
import json
import logging
from typing import Dict, Any, Callable, List, Optional
from datetime import datetime
import uuid
from enum import Enum
import os

logger = logging.getLogger(__name__)

class EventPriority(Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3

class Event:
    """Domain Event padrão"""
    def __init__(
        self,
        type: str,
        data: Any = None,
        priority: EventPriority = EventPriority.NORMAL,
        source: str = None,
        correlation_id: str = None
    ):
        self.id = str(uuid.uuid4())
        self.type = type
        self.data = data
        self.priority = priority
        self.source = source
        self.correlation_id = correlation_id or str(uuid.uuid4())
        self.timestamp = datetime.utcnow().isoformat()
        self.version = "1.0"
    
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "data": self.data,
            "priority": self.priority.value,
            "source": self.source,
            "correlation_id": self.correlation_id,
            "timestamp": self.timestamp,
            "version": self.version
        }

class EventBus:
    """Event Bus universal - In-memory com Redis fallback"""
    
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
        self._global_handlers: List[Callable] = []
        self._event_store: List[Dict[str, Any]] = []
        self._use_redis = False
        self._redis_client = None
        
        # Tenta Redis
        self._init_redis()
    
    def _init_redis(self):
        try:
            import redis.asyncio as redis
            redis_url = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
            if redis_url:
                self._redis_client = redis.from_url(redis_url, decode_responses=True)
                self._use_redis = True
                logger.info("✅ Redis event bus initialized")
        except Exception as e:
            logger.debug(f"Redis not available, using in-memory: {e}")
    
    async def publish(self, event_type: str, data: Any = None, **kwargs):
        """Publica evento"""
        event = Event(event_type, data, **kwargs)
        
        # Store locally
        self._event_store.append(event.to_dict())
        if len(self._event_store) > 1000:
            self._event_store.pop(0)
        
        # Publica no Redis se disponível
        if self._use_redis and self._redis_client:
            try:
                await self._redis_client.publish("events", json.dumps(event.to_dict()))
            except Exception as e:
                logger.warning(f"Redis publish failed: {e}")
        
        # Processa localmente
        await self._process_locally(event)
        
        logger.info(f"📢 Event published: {event_type}")
        return event
    
    async def _process_locally(self, event: Event):
        """Processa evento localmente"""
        # Handlers específicos
        if event.type in self._handlers:
            for handler in self._handlers[event.type]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(event)
                    else:
                        handler(event)
                except Exception as e:
                    logger.error(f"Handler error for {event.type}: {e}")
        
        # Handlers globais
        for handler in self._global_handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as e:
                logger.error(f"Global handler error: {e}")
    
    def subscribe(self, event_type: str, handler: Callable):
        """Subscribe to specific event type"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
    
    def subscribe_all(self, handler: Callable):
        """Subscribe to all events"""
        self._global_handlers.append(handler)
    
    def get_recent_events(self, limit: int = 100) -> list:
        """Get recent events"""
        return self._event_store[-limit:]
    
    def get_events_by_type(self, event_type: str) -> list:
        """Filter events by type"""
        return [e for e in self._event_store if e.get("type") == event_type]
    
    async def close(self):
        """Clean up resources"""
        if self._redis_client:
            await self._redis_client.close()

# Singleton
_event_bus: Optional[EventBus] = None

def get_event_bus() -> EventBus:
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus

# Aliases para compatibilidade
def get_recent_events(limit: int = 100) -> list:
    """Get recent events"""
    return get_event_bus().get_recent_events(limit)

def get_events_by_type(event_type: str) -> list:
    """Filter events by type"""
    return get_event_bus().get_events_by_type(event_type)

__all__ = [
    'EventBus', 'get_event_bus', 'Event', 'EventPriority',
    'get_recent_events', 'get_events_by_type'
]
