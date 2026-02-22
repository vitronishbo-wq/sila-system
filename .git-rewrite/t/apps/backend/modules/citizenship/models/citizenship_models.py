"""
Modelos SQLAlchemy para o módulo de Cidadania.

Define as entidades principais para:
- Catálogo de serviços disponíveis
- Controle de solicitações de serviços
- Relacionamentos com cidadãos e documentos
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import backref, relationship

from core.db.base_class import Base  # Use centralized Base

from ..schemas.citizenship import PriorityLevel, ServiceCategory, ServiceStatus

# Remove local Base creation


class CitizenshipService(Base):
    """
    Modelo para serviços disponíveis no catálogo de cidadania.

    Define os serviços que podem ser solicitados pelos cidadãos,
    incluindo informações sobre prazos, requisitos e categorias.
    """

    __tablename__ = "citizenship_services"

    __table_args__ = {"extend_existing": True}

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(Enum(ServiceCategory), nullable=False)
    estimated_days = Column(Integer, nullable=False)
    requirements = Column(Text)  # JSON array como string
    is_active = Column(Boolean, default=True, nullable=False)
    priority = Column(Enum(PriorityLevel), default=PriorityLevel.NORMAL)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relacionamentos
    # FIXED: Removed problematic circular relationship that conflicts with ServiceRequest.service
    # requests = relationship("ServiceRequest", foreign_keys="ServiceRequest.service_id", back_populates="service")

    def __repr__(self):
        return f"<CitizenshipService(id={self.id}, code='{self.code}', name='{self.name}')>"


class ServiceRequest(Base):
    """
    Modelo para solicitações de serviços de cidadania.

    Controla todas as solicitações feitas pelos cidadãos,
    incluindo status, protocolo e informações de contato.
    """

    __tablename__ = "citizenship_service_requests"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    citizen_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey("citizenship_citizens.id"),
        nullable=False,
        index=True,
    )
    service_id = Column(
        PGUUID(as_uuid=True), ForeignKey("citizenship_services.id"), nullable=False
    )

    # Dados da solicitação
    protocol_number = Column(String(50), unique=True, nullable=False, index=True)
    status = Column(Enum(ServiceStatus), default=ServiceStatus.PENDING, nullable=False)
    priority = Column(Enum(PriorityLevel), default=PriorityLevel.NORMAL)

    # Informações de contato e observações
    observations = Column(Text)
    contact_phone = Column(String(20))
    contact_email = Column(String(100))

    # Controle de prazos
    estimated_completion = Column(DateTime)
    completed_at = Column(DateTime)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relacionamentos
    service = relationship(
        "CitizenshipService", foreign_keys=[service_id]
    )  # Removed back_populates due to circular reference
    citizen = relationship(
        "Citizen", foreign_keys=[citizen_id], backref=backref("service_requests", lazy="dynamic")
    )

    def __repr__(self):
        return f"<ServiceRequest(id={self.id}, protocol='{self.protocol_number}', status={self.status})>"


class ServiceRequestHistory(Base):
    """
    Modelo para histórico de alterações de status das solicitações.

    Mantém um log completo de todas as mudanças de status
    para auditoria e rastreabilidade.
    """

    __tablename__ = "citizenship_service_request_history"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    request_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey("citizenship_service_requests.id"),
        nullable=False,
    )

    # Dados da alteração
    old_status = Column(Enum(ServiceStatus))
    new_status = Column(Enum(ServiceStatus), nullable=False)
    changed_by = Column(String(100), nullable=False)  # ID ou nome do usuário
    change_reason = Column(Text)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relacionamentos
    request = relationship("ServiceRequest", backref=backref("history", lazy="dynamic"))

    def __repr__(self):
        return f"<ServiceRequestHistory(id={self.id}, request_id={self.request_id}, new_status={self.new_status})>"
