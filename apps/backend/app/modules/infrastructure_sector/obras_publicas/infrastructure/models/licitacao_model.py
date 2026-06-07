"""Licitacao model for Obras Públicas."""

import uuid

from sqlalchemy import UUID, Column, DateTime, Float, ForeignKey, String
from sqlalchemy.sql import func

from apps.backend.app.core.db import Base


class LicitacaoModel(Base):
    """Modelo SQLAlchemy para Licitação (Bidding)."""

    __tablename__ = "obras_publicas_licitacoes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_licitacao = Column(String(100), unique=True, nullable=False, index=True)
    edital_id = Column(
        UUID(as_uuid=True), ForeignKey("obras_publicas_editais.id"), nullable=False, index=True
    )
    tipo = Column(String(50), nullable=False, index=True)
    status = Column(String(50), default="PREPARACAO", index=True)
    valor_estimado = Column(Float, nullable=True)
    data_abertura = Column(DateTime, nullable=True)
    data_resultado = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
