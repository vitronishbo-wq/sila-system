from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.domain.db import Base


class TrafficViolationModel(Base):
    __tablename__ = "traffic_violations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    citizen_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    vehicle_plate: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    violation_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fine_amount: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(8), nullable=False, server_default="Kz")
    status: Mapped[str] = mapped_column(String(32), nullable=False, server_default="PENDING", index=True)
    issued_by: Mapped[str | None] = mapped_column(String(100), nullable=True)
    source_service: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
