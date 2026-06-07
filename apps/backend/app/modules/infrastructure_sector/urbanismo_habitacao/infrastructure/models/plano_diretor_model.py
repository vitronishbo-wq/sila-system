from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import JSON, Date, DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class PlanoDiretorModel(Base):
    __tablename__ = "urbanismo_habitacao_planos_diretores"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_plano: Mapped[str] = mapped_column(String(40), unique=True, nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    provincia: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    ano_elaboracao: Mapped[int] = mapped_column(Integer, nullable=False)
    orgao_responsavel_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    municipio: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    ano_aprovacao: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ano_publicacao: Mapped[int | None] = mapped_column(Integer, nullable=True)
    periodo_validade_inicio: Mapped[date | None] = mapped_column(Date, nullable=True)
    periodo_validade_fim: Mapped[date | None] = mapped_column(Date, nullable=True)
    lei_aprovacao: Mapped[str | None] = mapped_column(String(120), nullable=True)
    participantes_consulta: Mapped[int | None] = mapped_column(Integer, nullable=True)
    audiencias_publicas: Mapped[int | None] = mapped_column(Integer, nullable=True)
    documento_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    mapa_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    area_total_urbana: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    area_total_rural: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    populacao_estimada: Mapped[int | None] = mapped_column(Integer, nullable=True)
    densidade_media: Mapped[Decimal | None] = mapped_column(Numeric(12, 4), nullable=True)
    macrozoneamento: Mapped[list[dict] | None] = mapped_column(JSON, nullable=True)
    diretrizes_gerais: Mapped[str | None] = mapped_column(Text, nullable=True)
    objetivos_estrategicos: Mapped[str | None] = mapped_column(Text, nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    data_publicacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
