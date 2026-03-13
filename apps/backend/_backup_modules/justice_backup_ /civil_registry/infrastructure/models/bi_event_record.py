"""
BIEvent ORM Model - Persistência de Eventos de Identidade Civil

Este modelo permite persistir eventos de domínio para auditoria e event sourcing.
"""
import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.modules.justice.civil_registry.shared.orm_base import Base

class BIEventRecord(Base):
    """
    Registro persistente de eventos de Identidade Civil.
    
    Cada evento é imutável após criação (append-only).
    Permite reconstrução do estado e auditoria completa.
    """
    __tablename__ = 'bi_events'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aggregate_id: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    event_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    operator_id: Mapped[str] = mapped_column(String(100), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    payload: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    event_metadata: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    def __repr__(self):
        return f'<BIEventRecord {self.event_type} on {self.aggregate_id}>'
