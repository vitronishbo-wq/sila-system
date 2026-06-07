from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class NotificationBase(BaseModel):
    citizen_id: str
    title: str | None = None
    message: str
    channel: str | None = None


class NotificationOut(NotificationBase):
    id: UUID

    class Config:
        from_attributes = True


class NotificationDeliveryBase(BaseModel):
    notification_id: UUID
    channel: str
    status: str
    delivered_at: datetime | None = None


class NotificationDeliveryOut(NotificationDeliveryBase):
    id: UUID

    class Config:
        from_attributes = True


class NotificationPreferenceBase(BaseModel):
    citizen_id: str
    channel: str
    enabled: bool = True


class NotificationPreferenceOut(NotificationPreferenceBase):
    id: UUID

    class Config:
        from_attributes = True


__all__ = [
    "NotificationBase",
    "NotificationOut",
    "NotificationDeliveryBase",
    "NotificationDeliveryOut",
    "NotificationPreferenceBase",
    "NotificationPreferenceOut",
]
