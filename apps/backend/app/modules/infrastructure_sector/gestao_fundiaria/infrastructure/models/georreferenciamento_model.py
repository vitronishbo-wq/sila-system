from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class GeorreferenciamentoModel(Base):
    __tablename__ = "gestao_fundiaria_georreferenciamentos"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_geo: Mapped[str] = mapped_column(String(60), unique=True, nullable=False, index=True)
    imovel_inscricao: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    latitude: Mapped[Decimal] = mapped_column(Numeric(12, 8), nullable=False)
    longitude: Mapped[Decimal] = mapped_column(Numeric(12, 8), nullable=False)
    sistema_referencia: Mapped[str] = mapped_column(String(24), nullable=False, index=True)
    data_registro: Mapped[date] = mapped_column(Date, nullable=False)
    precisao_metros: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    area_calculada: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    validado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    data_atualizacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
