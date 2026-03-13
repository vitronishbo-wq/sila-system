from __future__ import annotations
import uuid
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Date, DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.core.db import Base

class ProjetoModel(Base):
    __tablename__ = 'obras_publicas_projetos'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_projeto: Mapped[str] = mapped_column(String(40), unique=True, nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    orgao_responsavel_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    responsavel_tecnico_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    valor_estimado: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    data_inicio_prevista: Mapped[date] = mapped_column(Date, nullable=False)
    data_fim_prevista: Mapped[date] = mapped_column(Date, nullable=False)
    data_cadastro: Mapped[date] = mapped_column(Date, nullable=False)
    obra_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    data_inicio_real: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_fim_real: Mapped[date | None] = mapped_column(Date, nullable=True)
    versao: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    data_atualizacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)