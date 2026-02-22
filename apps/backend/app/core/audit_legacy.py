from sqlalchemy.orm import Session
from sqlalchemy import Column, String, DateTime, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
import logging
import threading
import inspect
from typing import List, Dict, Any

from app.core.database import Base

logger = logging.getLogger(__name__)

class ImmutableAuditLog:
    """In-memory immutable audit collector used in tests.

    API:
    - add(record: dict)
    - all() -> List[dict]
    - clear()
    """
    _lock = threading.Lock()
    _entries: List[Dict[str, Any]] = []

    @classmethod
    def add(cls, record: Dict[str, Any]):
        with cls._lock:
            # Store a shallow copy to keep immutability semantics
            cls._entries.append(dict(record))

    @classmethod
    def log(cls, **kwargs):
        """Convenience method used in tests and older code to append
        a simple audit record. Keeps backwards compatibility with
        callers that expect `ImmutableAuditLog.log(...)`.
        """
        record = dict(kwargs)
        record.setdefault("timestamp", datetime.utcnow().isoformat())
        cls.add(record)

    @classmethod
    def all(cls):
        with cls._lock:
            return list(cls._entries)

    @classmethod
    def clear(cls):
        with cls._lock:
            cls._entries.clear()

    @classmethod
    def get_entries(cls, **filters) -> List[Dict[str, Any]]:
        """Busca entradas filtradas (compatibilidade com testes)."""
        with cls._lock:
            results = cls._entries
            for key, value in filters.items():
                results = [e for e in results if e.get(key) == value]
            return results


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(String(100), unique=True)
    action = Column(String(100), nullable=False)
    actor_id = Column(String(100), nullable=True)
    actor_type = Column(String(50), nullable=True)
    resource_id = Column(String(100), nullable=True)
    resource_type = Column(String(50), nullable=True)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(250), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        # Accept kwargs and only set known mapped attributes.
        # This defensive constructor avoids failing when tests or
        # calling code pass attributes before instrumentation is
        # fully configured in complex test import orders.
        for k, v in kwargs.items():
            if hasattr(type(self), k):
                setattr(self, k, v)

async def audit_log(
    action: str,
    actor_id: str = None,
    actor_type: str = None,
    resource_id: str = None,
    resource_type: str = None,
    old_value: dict = None,
    new_value: dict = None,
    ip_address: str = None,
    user_agent: str = None,
    db = None
):
    """Regista auditoria REAL (Async)"""
    
    event_id = f"{datetime.utcnow().timestamp()}-{uuid.uuid4().hex[:8]}"
    
    log_entry = AuditLog(
        event_id=event_id,
        action=action,
        actor_id=actor_id,
        actor_type=actor_type,
        resource_id=resource_id,
        resource_type=resource_type,
        old_value=old_value,
        new_value=new_value,
        ip_address=ip_address,
        user_agent=user_agent,
        created_at=datetime.utcnow()
    )
    
    # Se tem DB, persiste (Suporta AsyncSession)
    if db:
        try:
            # Prefer a direct table insert to avoid relying on ORM mapping state
            # (avoids UnmappedInstanceError during complex test import orders).
            from sqlalchemy import insert
            tbl = Base.metadata.tables.get("audit_logs")
            payload = {
                "event_id": event_id,
                "action": action,
                "actor_id": actor_id,
                "actor_type": actor_type,
                "resource_id": resource_id,
                "resource_type": resource_type,
                "old_value": old_value,
                "new_value": new_value,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "created_at": datetime.utcnow(),
            }

            if tbl is not None:
                # Use core INSERT against the table
                if inspect.iscoroutinefunction(db.execute) or hasattr(db, "sync_session"):
                    # AsyncSession: use await
                    await db.execute(insert(tbl).values(**payload))
                else:
                    db.execute(insert(tbl).values(**payload))
                # commit if session exposes commit
                if hasattr(db, "commit"):
                    if inspect.iscoroutinefunction(db.commit):
                        await db.commit()
                    else:
                        db.commit()
            else:
                # Fallback to ORM add if table not present
                db.add(log_entry)
                if hasattr(db, "commit"):
                    if inspect.iscoroutinefunction(db.commit):
                        await db.commit()
                    else:
                        db.commit()
        except Exception as e:
            logger.error(f"Erro ao salvar auditoria: {e}")
            if hasattr(db, "rollback"):
                if inspect.iscoroutinefunction(db.rollback):
                    await db.rollback()
                else:
                    db.rollback()
    
    # Sempre log em arquivo também
    logger.info(f"AUDIT_ASYNC: {action} | Actor: {actor_id} | Resource: {resource_id}")
    
    # Publicar evento (Se publish_event for async, deve-se usar await)
    from app.core.events import publish_event
    res = publish_event(
        f"audit.{action.lower()}",
        {
            "event_id": event_id,
            "action": action,
            "actor_id": actor_id,
            "resource_id": resource_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    )
    if inspect.isawaitable(res):
        await res
    
    return event_id
