from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class ProdutoProcessadoModel(Base):
    __tablename__ = "pescas_industriais_produtos_processados"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_produto: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    unidade_processamento_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    nome_comercial: Mapped[str] = mapped_column(String(200), nullable=False)
    tipo_produto: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    tipo_processamento: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    peso_liquido_kg: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    rendimento_percentual: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    mercado_destino: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    data_registro: Mapped[date] = mapped_column(Date, nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
