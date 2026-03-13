from __future__ import annotations
import uuid
from datetime import datetime
from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.domain.db import Base

class DespachoModel(Base):
    __tablename__ = 'protecao_civil_despachos'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_despacho: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    ocorrencia_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    corporacao_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    bombeiro_responsavel_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default='gerado', index=True)
    data_despacho: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, index=True)
    data_ultima_atualizacao: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, index=True)
    meio_deslocamento: Mapped[str | None] = mapped_column(String(100), nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())