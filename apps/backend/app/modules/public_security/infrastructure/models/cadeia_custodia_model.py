from __future__ import annotations
import uuid
from datetime import datetime
from sqlalchemy import JSON, Boolean, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.domain.db import Base

class CadeiaCustodiaModel(Base):
    __tablename__ = 'seguranca_cadeias_custodia'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_cadeia: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    prova_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, unique=True, index=True)
    ocorrencia_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default='iniciada', index=True)
    local_atual: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    responsavel_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    data_inicio: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, index=True)
    data_ultima_movimentacao: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, index=True)
    historico_movimentacoes: Mapped[list[dict]] = mapped_column(JSON, nullable=False, default=list)
    integridade_verificada: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())