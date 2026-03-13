from __future__ import annotations
import uuid
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Boolean, Date, DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class IndicadorQualidadeModel(Base):
    __tablename__ = 'telecom_indicadores_qualidade'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_indicador: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    operadora_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    referencia_ano: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    referencia_mes: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    total_medicoes: Mapped[int] = mapped_column(Integer, nullable=False)
    disponibilidade_media_percentual: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    latencia_media_ms: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    jitter_medio_ms: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    perda_pacotes_media_percentual: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    conformidade_percentual: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    data_calculo: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())