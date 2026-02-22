# modules/payment/models/audit_log.py
"""Audit log model for payment operations."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, JSON, Text

from config.database import Base


class PaymentAuditLog(Base):
    __tablename__ = "payment_audit_logs"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(Integer, nullable=True, index=True)
    action = Column(String(50), nullable=False, index=True)
    user_id = Column(Integer, nullable=True)
    ip_address = Column(String(45), nullable=True)
    details = Column(JSON, nullable=True, default=dict)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    def __repr__(self) -> str:
        return f"<PaymentAuditLog(id={self.id}, payment_id={self.payment_id}, action='{self.action}')>"

    def __str__(self) -> str:
        return f"<AuditLog {self.action} on Payment {self.payment_id}>"
