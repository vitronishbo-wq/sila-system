from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import JSON, Date, DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class ZoneamentoModel(Base):
    __tablename__ = "urbanismo_habitacao_zoneamentos"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_zoneamento: Mapped[str] = mapped_column(
        String(40), unique=True, nullable=False, index=True
    )
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo_zona: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    plano_diretor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    provincia: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    usos_permitidos: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    municipio: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    coeficiente_aproveitamento_max: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 4), nullable=True
    )
    taxa_ocupacao_max: Mapped[Decimal | None] = mapped_column(Numeric(12, 4), nullable=True)
    gabarito_maximo: Mapped[int | None] = mapped_column(Integer, nullable=True)
    recuo_frontal_minimo: Mapped[Decimal | None] = mapped_column(Numeric(12, 4), nullable=True)
    permeabilidade_minima: Mapped[Decimal | None] = mapped_column(Numeric(12, 4), nullable=True)
    area_lote_minima: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    data_inicio_vigencia: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_cadastro: Mapped[date] = mapped_column(Date, nullable=False)
    data_atualizacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
