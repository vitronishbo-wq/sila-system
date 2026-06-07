from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from apps.backend.app.core.db import Base
from sqlalchemy import DateTime, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column


class EconomyInvoiceModel(Base):
    __tablename__ = "economy_invoices"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    citizen_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    reference: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    revenue_code: Mapped[str] = mapped_column(String(32), nullable=False)
    cost_center: Mapped[str] = mapped_column(String(32), nullable=False)
    service_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    service_name: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="AOA")
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    request_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
