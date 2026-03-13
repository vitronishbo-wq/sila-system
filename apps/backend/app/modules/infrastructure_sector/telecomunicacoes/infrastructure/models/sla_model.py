from __future__ import annotations
import uuid
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Boolean, Date, DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class SLAModel(Base):
    __tablename__ = 'telecom_slas'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_sla: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    operadora_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    servico: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    disponibilidade_min_percentual: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    latencia_max_ms: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    jitter_max_ms: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    perda_pacotes_max_percentual: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    velocidade_download_min_mbps: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    velocidade_upload_min_mbps: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    data_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    data_fim: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())