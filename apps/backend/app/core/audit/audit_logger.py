import logging
from typing import Any

logger = logging.getLogger("audit")


def audit_log(action: str, entity_id: str, request_id: str, metadata: dict[str, Any] | None = None):
    """Structured audit log with required request_id."""
    logger.info(
        "audit_event",
        extra={
            "action": action,
            "entity_id": entity_id,
            "request_id": request_id,
            "metadata": metadata or {},
        },
    )
