from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class FinancialAuditModel(Base):
    """
    Modelo de Persistência para Logs de Auditoria Financeira.
    """
    __tablename__ = "financial_audit_logs"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    entity_type: Mapped[str] = mapped_column(String(50), index=True) # 'INVOICE' ou 'PAYMENT'
    entity_id: Mapped[str] = mapped_column(String, index=True)
    action: Mapped[str] = mapped_column(String(100)) # 'STATUS_CHANGE', 'CREATION', 'VOID'
    
    previous_state: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    new_state: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    performed_by: Mapped[str] = mapped_column(String, index=True) # ID do User ou 'SYSTEM'
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)

    def __repr__(self) -> str:
        return f"<FinancialAuditModel({self.entity_type} {self.entity_id}: {self.action})>"
