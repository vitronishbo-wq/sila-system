from __future__ import annotations

import uuid

from apps.backend.app.core.db import Base
from sqlalchemy import DateTime, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column


class AcademicRecordModel(Base):
    __tablename__ = "educacao_academic_records"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    academic_identity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    current_class: Mapped[str | None] = mapped_column(String(32), nullable=True)
    completed_classes: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    sanctions: Mapped[list[dict]] = mapped_column(JSONB, nullable=False, default=list)
    debts: Mapped[list[dict]] = mapped_column(JSONB, nullable=False, default=list)
    history_json: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("academic_identity_id", name="uq_academic_record_identity"),
        {},
    )
