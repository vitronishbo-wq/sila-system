from datetime import datetime
import uuid
from sqlalchemy import DateTime, ForeignKey, JSON, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.domain.db import Base

class OperationalOrderModel(Base):
    __tablename__ = 'operational_orders'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    citizen_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    service_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('services.id', ondelete='RESTRICT'), index=True, nullable=False)
    workflow_instance_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False, default=uuid.uuid4)
    total_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True, default='DRAFT')
    status_history: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    receipt_number: Mapped[str | None] = mapped_column(String(64), unique=True, nullable=True)
    proof_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    documents: Mapped[list['OperationalOrderDocumentModel']] = relationship('OperationalOrderDocumentModel', back_populates='order', cascade='all, delete-orphan')
    payments: Mapped[list['OperationalPaymentModel']] = relationship('OperationalPaymentModel', back_populates='order', cascade='all, delete-orphan')

class OperationalOrderDocumentModel(Base):
    __tablename__ = 'operational_order_documents'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('operational_orders.id', ondelete='CASCADE'), index=True, nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(120), nullable=False)
    size_bytes: Mapped[int] = mapped_column(nullable=False)
    uri: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    order: Mapped['OperationalOrderModel'] = relationship('OperationalOrderModel', back_populates='documents')