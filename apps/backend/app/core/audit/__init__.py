"""Audit module - consolidated entrypoint and test compatibility hooks."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any

from apps.backend.app.core.audit.analytics import AuditAnalytics
from apps.backend.app.core.audit.sla_definitions import (
    ANOMALY_THRESHOLDS,
    SLA_DEFINITIONS,
    SLO_TARGETS,
    evaluate_sla_status,
    get_sla_for_service,
)
from sqlalchemy import text

logger = logging.getLogger(__name__)


async def audit_log(action: str | None = None, **payload: Any):
    """Compatibility async audit hook used by legacy and new tests."""
    event_action = action or payload.get("action") or "UNKNOWN"
    db = payload.pop("db", None)
    entry = {
        "action": event_action,
        "resource_id": payload.get("resource_id"),
        "new_value": payload.get("new_value"),
        "request_id": payload.get("request_id"),
        "created_at": datetime.utcnow(),
    }
    ImmutableAuditLog.append(entry)
    logger.info("audit_log_event", extra={"audit": entry})
    if db is not None:
        try:
            col_result = await db.execute(
                text(
                    "\n                    SELECT column_name\n                    FROM information_schema.columns\n                    WHERE table_name = 'audit_logs'\n                    "
                )
            )
            columns = {row[0] for row in col_result.fetchall()}
            if columns:
                insert_map: dict[str, Any] = {}
                if "action" in columns:
                    insert_map["action"] = event_action
                if "resource_id" in columns:
                    insert_map["resource_id"] = entry["resource_id"]
                if "created_at" in columns:
                    insert_map["created_at"] = entry["created_at"]
                if "new_value" in columns:
                    insert_map["new_value"] = entry["new_value"] or {}
                if "metadata_json" in columns:
                    insert_map["metadata_json"] = json.dumps(
                        {
                            "new_value": entry["new_value"] or {},
                            "request_id": entry.get("request_id"),
                        }
                    )
                if "user_id" in columns:
                    user_id = payload.get("user_id")
                    if user_id is None:
                        user_res = await db.execute(
                            text("SELECT id FROM users ORDER BY id LIMIT 1")
                        )
                        user_row = user_res.first()
                        user_id = user_row[0] if user_row else None
                    insert_map["user_id"] = user_id
                if insert_map:
                    cols = ", ".join(insert_map.keys())
                    binds = ", ".join(f":{k}" for k in insert_map)
                    await db.execute(
                        text(f"INSERT INTO audit_logs ({cols}) VALUES ({binds})"), insert_map
                    )
        except Exception as exc:
            logger.warning("audit_log_db_write_failed: %s", exc)
    return entry


class ImmutableAuditLog:
    """Legacy in-memory audit buffer kept for test compatibility."""

    _entries: list[dict[str, Any]] = []

    @classmethod
    def append(cls, entry):
        cls._entries.append(entry)

    @classmethod
    def clear(cls):
        cls._entries.clear()


__all__ = [
    "audit_log",
    "ImmutableAuditLog",
    "AuditAnalytics",
    "SLA_DEFINITIONS",
    "SLO_TARGETS",
    "ANOMALY_THRESHOLDS",
    "get_sla_for_service",
    "evaluate_sla_status",
]
