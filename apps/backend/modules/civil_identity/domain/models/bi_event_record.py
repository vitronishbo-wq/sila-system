"""
BIEvent ORM Model - Persistência de Eventos de Identidade Civil

Este modelo permite persistir eventos de domínio para auditoria e event sourcing.
"""
import uuid
from datetime import datetime
from sqlalchemy import String, Text, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class BIEventRecord(Base):
    """
    Registro persistente de eventos de Identidade Civil.
    
    Cada evento é imutável após criação (append-only).
    Permite reconstrução do estado e auditoria completa.
    """
    __tablename__ = "bi_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    
    # Referência ao agregado (BI ou IdentityRequest)
    aggregate_id: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    
    # Tipo de evento (REQUEST_CREATED, BI_ISSUED, etc.)
    event_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    
    # Operador que executou a ação
    operator_id: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Timestamp do evento
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False, index=True
    )
    
    # Payload do evento (dados específicos)
    payload: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    
    # Metadados do sistema
    event_metadata: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    def __repr__(self):
        return f"<BIEventRecord {self.event_type} on {self.aggregate_id}>"
