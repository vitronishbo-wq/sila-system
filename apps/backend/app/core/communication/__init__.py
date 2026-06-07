"""Macro-domain: communication primitives."""

from apps.backend.app.core.events import EventPublisher, get_event_bus
from apps.backend.app.core.notifications.services.notification_service import NotificationService
from apps.backend.app.core.observability import Metrics, logger, trace

__all__ = ["EventPublisher", "Metrics", "NotificationService", "get_event_bus", "logger", "trace"]
