"""Frota model for Transport."""

import uuid

from sqlalchemy import UUID, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from apps.backend.app.core.db import Base


class FrotaModel(Base):
    """Modelo SQLAlchemy para Frota."""

    __tablename__ = "transporte_frota"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_frota = Column(String(100), unique=True, nullable=False, index=True)
    total_veiculos = Column(Integer, default=0)
    status = Column(String(50), default="ATIVO", index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
