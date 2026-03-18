from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base


class EconomyPaymentModel(Base):
    __tablename__ = 'economy_payments'

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    invoice_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    citizen_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default='AOA')
    gateway_reference: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    payment_method: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
