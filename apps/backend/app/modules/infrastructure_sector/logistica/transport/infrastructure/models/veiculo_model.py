"""Veiculo model for Transport."""

import uuid

from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from apps.backend.app.core.db import Base


class VeiculoModel(Base):
    """Modelo SQLAlchemy para Veículo."""

    __tablename__ = "transporte_veiculos"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_veiculo = Column(String(100), unique=True, nullable=False, index=True)
    placa = Column(String(50), unique=True, nullable=False)
    frota_id = Column(
        UUID(as_uuid=True), ForeignKey("transporte_frota.id"), nullable=False, index=True
    )
    capacidade = Column(Integer, nullable=True)
    status = Column(String(50), default="DISPONIVEL", index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
