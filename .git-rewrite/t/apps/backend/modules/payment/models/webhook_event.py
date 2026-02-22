"""Webhook event log model for tracking webhook deliveries."""

from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy import Column, DateTime, Integer, String, JSON, Boolean

from core.db.base_class import Base


class PaymentWebhookEvent(Base):
    """Log of webhook events and their delivery status."""

    __tablename__ = "payment_webhook_events"

    id = Column(Integer, primary_key=True, index=True)
    webhook_id = Column(Integer, nullable=False, index=True)
    payment_id = Column(Integer, nullable=True, index=True)
    event_type = Column(
        String(50), nullable=False
    )  # payment.created, payment.completed, etc.
    payload = Column(JSON, nullable=False)
    delivered = Column(Boolean, default=False, index=True)
    delivery_attempts = Column(Integer, default=0)
    last_error = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    delivered_at = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<PaymentWebhookEvent(id={self.id}, webhook_id={self.webhook_id}, event_type='{self.event_type}')>"

    def __str__(self) -> str:
        return f"<WebhookEvent {self.event_type}>"
