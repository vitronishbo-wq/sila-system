from __future__ import annotations
import uuid
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.domain.db import Base

class AtendimentoModel(Base):
    __tablename__ = 'protecao_civil_atendimentos'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_atendimento: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    despacho_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    ocorrencia_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default='iniciado', index=True)
    inicio_atendimento: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, index=True)
    fim_atendimento: Mapped[datetime | None] = mapped_column(DateTime(timezone=False), nullable=True, index=True)
    local_atendimento: Mapped[str] = mapped_column(String(255), nullable=False)
    resumo: Mapped[str | None] = mapped_column(Text, nullable=True)
    vitimas_atendidas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    desalojados_atendidos: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    obitos_confirmados: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    equipe_responsavel_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())