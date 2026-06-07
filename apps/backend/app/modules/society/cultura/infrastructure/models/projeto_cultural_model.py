from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class ProjetoCulturalModel(Base):
    __tablename__ = "cultura_projetos_culturais"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_projeto: Mapped[str] = mapped_column(String(60), unique=True, nullable=False, index=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    natureza: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    proponente_cpf_cnpj: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    proponente_nome: Mapped[str] = mapped_column(String(200), nullable=False)
    resumo: Mapped[str] = mapped_column(Text, nullable=False)
    valor_solicitado: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    valor_aprovado: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    data_submissao: Mapped[date] = mapped_column(Date, nullable=False)
    data_inicio: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_fim: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    edital_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    justificativa: Mapped[str | None] = mapped_column(Text, nullable=True)
    objetivos: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
