"""Notification layer - Multi-channel notification support"""

from .notification_service import (
    NotificationService,
    Notification,
    NotificationType,
    NotificationStatus,
    NotificationProvider,
    get_notification_service,
)
from .email_provider import EmailProvider, SendgridEmailProvider
from .sms_provider import (
    SMSProvider,
    TwilioSMSProvider,
    AfricasTalkingSMSProvider,
    MockSMSProvider,
)
from .push_provider import (
    PushProvider,
    FirebasePushProvider,
    OneSignalPushProvider,
    MockPushProvider,
)

__all__ = [
    'NotificationService',
    'Notification',
    'NotificationType',
    'NotificationStatus',
    'NotificationProvider',
    'get_notification_service',
    'EmailProvider',
    'SendgridEmailProvider',
    'SMSProvider',
    'TwilioSMSProvider',
    'AfricasTalkingSMSProvider',
    'MockSMSProvider',
    'PushProvider',
    'FirebasePushProvider',
    'OneSignalPushProvider',
    'MockPushProvider',
]
