from __future__ import annotations

from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from apps.backend.app.core.db import Base


class Notification(Base):
    __tablename__ = "notifications"
    __table_args__ = {"extend_existing": True}
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    citizen_id = Column(String, nullable=False)
    title = Column(String, nullable=True)
    message = Column(Text, nullable=False)
    channel = Column(String, nullable=True)


class NotificationDelivery(Base):
    __tablename__ = "notification_deliveries"
    __table_args__ = {"extend_existing": True}
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    notification_id = Column(
        PGUUID(as_uuid=True), ForeignKey("notifications.id", ondelete="CASCADE"), nullable=False
    )
    channel = Column(String, nullable=False)
    status = Column(String, nullable=False)
    delivered_at = Column(DateTime, nullable=True)


class NotificationPreference(Base):
    __tablename__ = "notification_preferences"
    __table_args__ = {"extend_existing": True}
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    citizen_id = Column(String, nullable=False)
    channel = Column(String, nullable=False)
    enabled = Column(Boolean, nullable=False, default=True)


__all__ = ["Notification", "NotificationDelivery", "NotificationPreference"]
