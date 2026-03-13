from __future__ import annotations
import uuid
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Date, DateTime, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class FaturaTelecomModel(Base):
    __tablename__ = 'telecom_faturas'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_fatura: Mapped[str] = mapped_column(String(60), unique=True, nullable=False, index=True)
    assinante_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    referencia: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    consumo_total_gb: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    franquia_gb: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    excedente_gb: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    valor_plano: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    valor_excedente: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    valor_total: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    data_emissao: Mapped[date] = mapped_column(Date, nullable=False)
    data_vencimento: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    data_pagamento: Mapped[date | None] = mapped_column(Date, nullable=True)
    valor_pago: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())