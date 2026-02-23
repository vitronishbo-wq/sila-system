import enum
import uuid
from datetime import datetime
from typing import Any, Dict

from sqlalchemy import String, Enum, DateTime, Text, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.citizen.permissions.policies import DataSegment

class EventType(str, enum.Enum):
    BIRTH_REGISTRATION = "BIRTH_REGISTRATION"
    ID_CARD_ISSUED = "ID_CARD_ISSUED"
    PASSPORT_ISSUED = "PASSPORT_ISSUED"
    DRIVER_LICENSE_GRANTED = "DRIVER_LICENSE_GRANTED"
    MARRIAGE_REGISTRATION = "MARRIAGE_REGISTRATION"
    ADDRESS_UPDATE = "ADDRESS_UPDATE"
    VITAL_STATUS_CHANGE = "VITAL_STATUS_CHANGE"
    CRIMINAL_RECORD_UPDATE = "CRIMINAL_RECORD_UPDATE"
    PROPERTY_REGISTERED = "PROPERTY_REGISTERED"
    DEATH_REGISTRATION = "DEATH_REGISTRATION"

class CitizenEventModel(Base):
    __tablename__ = "fuc_events"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4,
        comment="Identificador único do evento (Hash de auditoria)"
    )
    citizen_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        index=True, 
        nullable=False,
        comment="Referência ao ID imutável do cidadão"
    )
    event_type: Mapped[EventType] = mapped_column(
        Enum(EventType), 
        nullable=False,
        index=True,
        comment="Tipo de ocorrência na vida civil"
    )
    payload: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, 
        nullable=False,
        comment="Dados específicos do evento em formato JSON binário"
    )
    legal_basis: Mapped[str] = mapped_column(
        Text, 
        nullable=False,
        comment="Fundamentação jurídica ou norma que autoriza o registro"
    )
    service_id: Mapped[str] = mapped_column(
        String(100), 
        index=True, 
        nullable=False,
        comment="ID do sistema/serviço originador (ex: REGISTO_CIVIL_01)"
    )
    performed_by: Mapped[str] = mapped_column(
        String(100), 
        nullable=False,
        comment="Identificação do agente público ou sistema que assinou o evento"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow,
        index=True,
        comment="Timestamp canônico da ocorrência (UTC)"
    )
    __table_args__ = (
        Index("idx_citizen_event_chronology", "citizen_id", "created_at"),
    )
    def __repr__(self) -> str:
        return f"<CitizenEvent(id={self.id}, type={self.event_type}, citizen={self.citizen_id})>"
