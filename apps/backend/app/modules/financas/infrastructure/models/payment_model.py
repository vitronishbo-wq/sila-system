from datetime import datetime
from typing import Optional
from sqlalchemy import String, Numeric, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.database import Base
from app.modules.financas.domain.models.enums import PaymentStatus

class PaymentModel(Base):
    """
    Modelo de Persistência para Pagamentos.
    """
    __tablename__ = "financas_payments"
    __table_args__ = {'extend_existing': True}

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    
    invoice_id: Mapped[str] = mapped_column(
        String, 
        ForeignKey("financas_invoices.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    
    citizen_id: Mapped[str] = mapped_column(String, index=True, nullable=False)
    
    amount: Mapped[float] = mapped_column(Numeric(precision=15, scale=2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="AOA", nullable=False)
    
    gateway_reference: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus, values_callable=lambda x: [e.value for e in x], native_enum=False), default=PaymentStatus.PENDING, nullable=False, index=True)
    payment_method: Mapped[str] = mapped_column(String, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    confirmed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    invoice: Mapped["InvoiceModel"] = relationship("InvoiceModel", back_populates="payments")

    def __repr__(self) -> str:
        return f"<PaymentModel(id={self.id}, invoice_id={self.invoice_id}, amount={self.amount})>"
