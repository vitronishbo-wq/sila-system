"""Projeto model for Obras Públicas."""

import uuid

from sqlalchemy import UUID, Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.sql import func

from apps.backend.app.core.db import Base


class ProjetoModel(Base):
    """Modelo SQLAlchemy para Projeto (Project)."""

    __tablename__ = "obras_publicas_projetos"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_projeto = Column(String(100), unique=True, nullable=False, index=True)
    obra_id = Column(
        UUID(as_uuid=True), ForeignKey("obras_publicas_obras.id"), nullable=False, index=True
    )
    titulo = Column(String(500), nullable=False)
    descricao = Column(Text, nullable=True)
    valor = Column(Float, nullable=True)
    data_inicio = Column(DateTime, nullable=True)
    data_conclusao_prevista = Column(DateTime, nullable=True)
    Status = Column(String(50), default="PLANEJAMENTO", index=True)
    responsavel_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
