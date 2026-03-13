from __future__ import annotations
import uuid
from datetime import datetime
from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.core.db import Base

class VestigioModel(Base):
    __tablename__ = 'seguranca_vestigios'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_vestigio: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    cadeia_custodia_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    ocorrencia_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    localizacao: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    data_coleta: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default='coletado', index=True)
    coletado_por_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())