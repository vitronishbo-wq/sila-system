from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Numeric, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.database import Base
from app.modules.financas.domain.models.enums import InvoiceStatus

class InvoiceModel(Base):
    """
    Modelo de Persistência para Faturas.
    """
    __tablename__ = "financas_invoices"
    __table_args__ = {'extend_existing': True}

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    citizen_id: Mapped[str] = mapped_column(String, index=True, nullable=False)
    request_id: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    reference: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    
    revenue_code: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    cost_center: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    
    service_code: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    service_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    amount: Mapped[float] = mapped_column(Numeric(precision=15, scale=2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="AOA", server_default="AOA", nullable=False)
    status: Mapped[InvoiceStatus] = mapped_column(Enum(InvoiceStatus, values_callable=lambda x: [e.value for e in x], native_enum=False), default=InvoiceStatus.PENDING, index=True, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    paid_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    payments: Mapped[List["PaymentModel"]] = relationship("PaymentModel", back_populates="invoice", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<InvoiceModel(ref={self.reference}, amount={self.amount}, status={self.status})>"
