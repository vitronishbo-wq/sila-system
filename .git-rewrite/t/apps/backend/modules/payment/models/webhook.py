"""Webhook model for payment events."""

from datetime import datetime
from typing import List

from sqlalchemy import Column, DateTime, Integer, String, Boolean, JSON

from core.db.base_class import Base


class PaymentWebhook(Base):
    """Webhook configuration for payment events."""

    __tablename__ = "payment_webhooks"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False)
    events = Column(JSON, nullable=False, default=[])  # List of event types
    active = Column(Boolean, default=True, nullable=False, index=True)
    secret_key = Column(String(255), nullable=True)  # For HMAC signature
    retry_count = Column(Integer, default=0)
    last_triggered_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<PaymentWebhook(id={self.id}, url='{self.url}', active={self.active})>"

    def __str__(self) -> str:
        return f"<Webhook {self.url}>"
