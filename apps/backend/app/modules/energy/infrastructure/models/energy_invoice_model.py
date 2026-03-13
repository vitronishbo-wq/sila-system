from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Date, DateTime, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class EnergyInvoiceModel(Base):
    __tablename__ = "energy_invoices"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    numero_fatura: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    consumo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    unidade_consumidora_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    cpf_titular: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    mes_referencia: Mapped[str] = mapped_column(String(16), nullable=False, index=True)

    consumo_kwh: Mapped[Decimal] = mapped_column(Numeric(14, 3), nullable=False)
    tarifa_kwh: Mapped[Decimal] = mapped_column(Numeric(14, 6), nullable=False)
    bandeira_tarifaria: Mapped[str] = mapped_column(String(32), nullable=False)
    valor_consumo: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    valor_bandeira: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    valor_iluminacao_publica: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    valor_total: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)

    data_emissao: Mapped[date] = mapped_column(Date, nullable=False)
    data_vencimento: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)

    data_pagamento: Mapped[date | None] = mapped_column(Date, nullable=True)
    valor_pago: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    metodo_pagamento: Mapped[str | None] = mapped_column(String(64), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
