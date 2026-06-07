"""Example Event Handler - logs events to observability pipeline - Phase 19"""

from typing import Any

from apps.backend.app.core.events.handlers.event_handler import EventHandler
from apps.backend.app.core.observability.enterprise_logging import get_logger

logger = get_logger("events.handlers.audit_logger")


class AuditLogEventHandler(EventHandler):
    """Log all events for audit trail"""

    @property
    def event_type(self) -> str:
        return "*"

    async def handle(self, event: dict[str, Any]):
        """Log event details"""
        logger.info(
            "domain_event",
            extra={
                "event_name": event.get("name"),
                "event_id": event.get("id"),
                "payload": event.get("payload"),
                "metadata": event.get("metadata"),
            },
        )


class UserAuthenticationEventHandler(EventHandler):
    """Handle user authentication events"""

    @property
    def event_type(self) -> str:
        return "USER_LOGGED_IN"

    async def handle(self, event: dict[str, Any]):
        """Process USER_LOGGED_IN event"""
        payload = event.get("payload", {})
        user_id = payload.get("user_id")
        logger.info("user_authenticated", extra={"user_id": user_id, "event_id": event.get("id")})
