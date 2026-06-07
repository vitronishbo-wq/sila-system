import asyncio
from typing import Any


class NotificationServiceAdapter:
    """Compatibility adapter for notification dispatch."""

    def __init__(self, notification_service: Any = None):
        self.notification_service = notification_service

    def send_notification(self, payload: dict) -> dict:
        if self.notification_service and hasattr(self.notification_service, "send_notification"):
            result = self.notification_service.send_notification(payload)
            return result or {}
        return {}

    def list_notifications(self, citizen_id: str) -> list:
        if self.notification_service and hasattr(self.notification_service, "list_notifications"):
            result = self.notification_service.list_notifications(citizen_id)
            return result or []
        return []

    async def get_notifications(self, citizen_id) -> dict:
        if self.notification_service and hasattr(self.notification_service, "get_notifications"):
            result = self.notification_service.get_notifications(citizen_id)
            if asyncio.iscoroutine(result):
                result = await result
            if isinstance(result, dict):
                result.setdefault("citizen_id", str(citizen_id))
                result.setdefault("notifications", [])
                return result
            return {"citizen_id": str(citizen_id), "notifications": []}
        return {"citizen_id": str(citizen_id), "notifications": []}

    async def mark_as_read(self, notification_id) -> dict:
        if self.notification_service and hasattr(self.notification_service, "mark_as_read"):
            result = self.notification_service.mark_as_read(notification_id)
            if asyncio.iscoroutine(result):
                result = await result
            return result if isinstance(result, dict) else {}
        return {"notification_id": str(notification_id), "status": "read"}
