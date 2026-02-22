# notifications models module
# Este arquivo foi gerado automaticamente pelo script fix_module_structure.ps1

from modules.citizenship.models.citizen import Citizen
from .notification_models import (
    Notification,
    NotificationTemplate,
    NotificationDelivery,
    NotificationEvent,
    NotificationSettings,
    NotificationQueue,
    NotificationWebhook,
    NotificationAlert,
)

__all__ = [
    "Citizen",
    "Notification",
    "NotificationTemplate",
    "NotificationDelivery",
    "NotificationEvent",
    "NotificationSettings",
    "NotificationQueue",
    "NotificationWebhook",
    "NotificationAlert",
]
