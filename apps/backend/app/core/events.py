import logging
from typing import Dict, Any, Optional
from datetime import datetime

from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

@dataclass
class BaseEvent:
    event_id: str = field(default_factory=lambda: f"evt-{int(datetime.utcnow().timestamp())}")
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class CitizenValidated(BaseEvent):
    citizen_id: str = ""
    status: str = ""
    full_name: Optional[str] = None
    document_type: Optional[str] = None


@dataclass
class CitizenValidationFailed(BaseEvent):
    citizen_id: str = ""
    reason: str = ""
    details: Dict[str, Any] = field(default_factory=dict)

class EventPublisher:
    _subscribers = []
    _event_history = []

    @classmethod
    def subscribe(cls, event_type, handler):
        cls._subscribers.append((event_type, handler))

    @classmethod
    def clear(cls):
        cls._subscribers = []
        cls._event_history = []

    @classmethod
    async def publish(cls, event: Any):
        event_type = type(event).__name__
        logger.info(f"📢 Evento Publicado (Publisher): {event_type}")
        cls._event_history.append(event)
        
        # Chamada real aos handlers (simplificado)
        for sub_type, handler in cls._subscribers:
            if isinstance(event, sub_type):
                if callable(handler):
                    try:
                        import asyncio
                        if asyncio.iscoroutinefunction(handler):
                            await handler(event)
                        else:
                            handler(event)
                    except Exception as e:
                        logger.error(f"Erro no handler de evento: {e}")

        # Mantém compatibilidade com o store global
        _event_store.append({
            "type": event_type,
            "data": str(event),
            "timestamp": datetime.utcnow().isoformat(),
            "event_object": event
        })


# Store de eventos em memória (para simplicidade)
# Em produção: usar Redis/RabbitMQ
_event_store = []

def publish_event(event_type: str, payload: Dict[str, Any], source: str = "system"):
    """Publica evento real"""
    event = {
        "id": f"{datetime.utcnow().timestamp()}-{hash(str(payload))}",
        "type": event_type,
        "source": source,
        "payload": payload,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    _event_store.append(event)
    logger.info(f"📢 Evento publicado: {event_type}")
    
    # Handlers específicos
    if event_type == "citizen.request.created":
        _handle_request_created(payload)
    elif event_type == "payment.processed":
        _handle_payment_processed(payload)
    
    return event

def _handle_request_created(payload: Dict[str, Any]):
    """Handler real para pedido criado"""
    logger.info(f"Novo pedido: {payload.get('request_id')}")

def _handle_payment_processed(payload: Dict[str, Any]):
    """Handler real para pagamento"""
    logger.info(f"Pagamento processado: {payload.get('transaction_id')}")

def get_recent_events(limit: int = 100) -> list:
    """Retorna eventos recentes"""
    return _event_store[-limit:]

def get_events_by_type(event_type: str) -> list:
    """Filtra eventos por tipo"""
    return [e for e in _event_store if e["type"] == event_type]
