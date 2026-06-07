from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class LoteamentoModel(Base):
    __tablename__ = "urbanismo_habitacao_loteamentos"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_loteamento: Mapped[str] = mapped_column(
        String(40), unique=True, nullable=False, index=True
    )
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    parcelamento_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    plano_diretor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    zoneamento_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    provincia: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    area_total: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    quantidade_lotes_prevista: Mapped[int] = mapped_column(Integer, nullable=False)
    municipio: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    quantidade_lotes_implantada: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    area_lotes: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    area_verde: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    area_institucional: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    data_inicio_prevista: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_fim_prevista: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_inicio_real: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_fim_real: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_cadastro: Mapped[date] = mapped_column(Date, nullable=False)
    data_atualizacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
