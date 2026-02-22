"""Notification Service Orchestrator"""

from enum import Enum
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
from datetime import datetime


class NotificationType(str, Enum):
    """Notification types"""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class NotificationStatus(str, Enum):
    """Notification status"""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"


class Notification:
    """Base notification model"""
    
    def __init__(
        self,
        recipient: str,
        subject: str,
        body: str,
        notification_type: NotificationType,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.id = f"{notification_type.value}_{datetime.now().timestamp()}"
        self.recipient = recipient
        self.subject = subject
        self.body = body
        self.notification_type = notification_type
        self.metadata = metadata or {}
        self.status = NotificationStatus.PENDING
        self.created_at = datetime.now()
        self.sent_at: Optional[datetime] = None
        self.error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'recipient': self.recipient,
            'subject': self.subject,
            'body': self.body,
            'type': self.notification_type.value,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'error': self.error,
            'metadata': self.metadata,
        }


class NotificationProvider(ABC):
    """Base notification provider"""
    
    @abstractmethod
    async def send(self, notification: Notification) -> bool:
        """Send notification"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check provider health"""
        pass


class NotificationService:
    """Orchestrate notifications across multiple providers"""
    
    def __init__(self):
        self._providers: Dict[NotificationType, NotificationProvider] = {}
        self._notification_queue: List[Notification] = []
    
    def register_provider(
        self,
        notification_type: NotificationType,
        provider: NotificationProvider,
    ):
        """Register notification provider"""
        self._providers[notification_type] = provider
    
    async def send(self, notification: Notification) -> bool:
        """Send notification through appropriate provider"""
        provider = self._providers.get(notification.notification_type)
        
        if not provider:
            notification.status = NotificationStatus.FAILED
            notification.error = f"No provider for {notification.notification_type.value}"
            return False
        
        try:
            success = await provider.send(notification)
            if success:
                notification.status = NotificationStatus.SENT
                notification.sent_at = datetime.now()
            else:
                notification.status = NotificationStatus.FAILED
            return success
        except Exception as e:
            notification.status = NotificationStatus.FAILED
            notification.error = str(e)
            return False
    
    async def send_email(
        self,
        recipient: str,
        subject: str,
        body: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Convenience method to send email"""
        notification = Notification(
            recipient=recipient,
            subject=subject,
            body=body,
            notification_type=NotificationType.EMAIL,
            metadata=metadata,
        )
        return await self.send(notification)
    
    async def send_sms(
        self,
        recipient: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Convenience method to send SMS"""
        notification = Notification(
            recipient=recipient,
            subject="SMS",
            body=message,
            notification_type=NotificationType.SMS,
            metadata=metadata,
        )
        return await self.send(notification)
    
    async def send_push(
        self,
        recipient: str,
        title: str,
        body: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Convenience method to send push"""
        notification = Notification(
            recipient=recipient,
            subject=title,
            body=body,
            notification_type=NotificationType.PUSH,
            metadata=metadata,
        )
        return await self.send(notification)
    
    async def send_bulk(self, notifications: List[Notification]) -> Dict[str, bool]:
        """Send multiple notifications"""
        results = {}
        for notification in notifications:
            results[notification.id] = await self.send(notification)
        return results
    
    async def health_check(self) -> Dict[NotificationType, bool]:
        """Check health of all providers"""
        health = {}
        for notification_type, provider in self._providers.items():
            try:
                health[notification_type] = await provider.health_check()
            except Exception:
                health[notification_type] = False
        return health
    
    async def get_notification_status(self, notification_id: str) -> Optional[Notification]:
        """Get notification status from queue"""
        for notification in self._notification_queue:
            if notification.id == notification_id:
                return notification
        return None
    
    def queue_notification(self, notification: Notification) -> None:
        """Add notification to queue"""
        self._notification_queue.append(notification)
    
    def get_queue(self, status: Optional[NotificationStatus] = None) -> List[Notification]:
        """Get notifications from queue"""
        if status:
            return [n for n in self._notification_queue if n.status == status]
        return self._notification_queue.copy()
    
    def clear_queue(self) -> int:
        """Clear notification queue"""
        count = len(self._notification_queue)
        self._notification_queue.clear()
        return count


# Singleton instance
_service_instance: Optional[NotificationService] = None


def get_notification_service() -> NotificationService:
    """Get notification service instance"""
    global _service_instance
    if _service_instance is None:
        _service_instance = NotificationService()
    return _service_instance
