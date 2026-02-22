"""Audit log model for payment operations."""

from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy import Column, DateTime, Integer, String, JSON, Text

from core.db.base_class import Base


class PaymentAuditLog(Base):
    """Audit log for payment operations."""

    __tablename__ = "payment_audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(Integer, nullable=True, index=True)
    action = Column(
        String(50), nullable=False, index=True
    )  # create, update, refund, delete, etc.
    user_id = Column(Integer, nullable=True)
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    details = Column(JSON, nullable=True, default={})
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    def __repr__(self) -> str:
        return f"<PaymentAuditLog(id={self.id}, payment_id={self.payment_id}, action='{self.action}')>"

    def __str__(self) -> str:
        return f"<AuditLog {self.action} on Payment {self.payment_id}>"
