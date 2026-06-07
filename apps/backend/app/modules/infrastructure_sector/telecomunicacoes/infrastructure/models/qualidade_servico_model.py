from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class QualidadeServicoModel(Base):
    __tablename__ = "telecom_qualidade_servico"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_medicao: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    operadora_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    assinante_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    sla_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    servico: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    data_medicao: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    disponibilidade_percentual: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    latencia_ms: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    jitter_ms: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    perda_pacotes_percentual: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    velocidade_download_mbps: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    velocidade_upload_mbps: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
