from __future__ import annotations
import uuid
from datetime import datetime
from sqlalchemy import DateTime, JSON, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.db import Base

class SagaInstanceModel(Base):
    __tablename__ = 'op_sagas'
    __table_args__ = (UniqueConstraint('tenant_id', 'saga_type', 'correlation_id', name='uq_op_sagas_tenant_type_correlation'),)
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    saga_type: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    correlation_id: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    tenant_id: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    state: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    data: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)