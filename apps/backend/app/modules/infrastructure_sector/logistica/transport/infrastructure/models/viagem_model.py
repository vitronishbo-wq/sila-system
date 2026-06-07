"""Viagem model for Transport."""

import uuid

from sqlalchemy import UUID, Column, DateTime, ForeignKey, String
from sqlalchemy.sql import func

from apps.backend.app.core.db import Base


class ViagemModel(Base):
    """Modelo SQLAlchemy para Viagem."""

    __tablename__ = "transporte_viagens"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_viagem = Column(String(100), unique=True, nullable=False, index=True)
    veiculo_id = Column(
        UUID(as_uuid=True), ForeignKey("transporte_veiculos.id"), nullable=False, index=True
    )
    linha_id = Column(
        UUID(as_uuid=True), ForeignKey("transporte_linhas.id"), nullable=False, index=True
    )
    data_saida = Column(DateTime, nullable=True)
    data_chegada = Column(DateTime, nullable=True)
    status = Column(String(50), default="PLANEJADA", index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
