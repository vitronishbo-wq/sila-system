from __future__ import annotations

import datetime
import json
import uuid
from collections.abc import Callable
from typing import Any


class AuditService:
    """Simple append-only audit service.

    This implementation writes JSON-lines to a local file under
    `data/` (append-only). In production swap the persistence via
    `AuditPort` to a proper immutable store.
    """

    def __init__(self, path: str | None = None) -> None:
        self.path = path or "data/foundation_audit.log"

    def log(self, entity_type: str, entity_id: str | None, action: str, actor: str | None,
            before: dict[str, Any] | None = None, after: dict[str, Any] | None = None,
            tenant_id: str | None = None) -> None:
        record = {
            "id": str(uuid.uuid4()),
            "ts": datetime.datetime.utcnow().isoformat() + "Z",
            "entity_type": entity_type,
            "entity_id": entity_id,
            "action": action,
            "actor": actor,
            "before": before,
            "after": after,
            "tenant_id": tenant_id,
        }
        line = json.dumps(record, default=str)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(line + "\n")


def audit(entity_type: str):
    """Decorator to audit a function call. Records before/after when possible.

    Usage:
        @audit("student")
        def update_student(...):
            ...
    """

    def deco(fn: Callable):
        def wrapper(*args, **kwargs):
            svc = AuditService()
            actor = kwargs.get("actor") or None
            entity_id = kwargs.get("entity_id") or None
            try:
                before = None
                result = fn(*args, **kwargs)
                after = result if isinstance(result, dict) else None
                svc.log(entity_type, entity_id, fn.__name__, actor, before=before, after=after)
                return result
            except Exception as exc:
                svc.log(entity_type, entity_id, fn.__name__ + ":error", actor, before=before, after={"error": str(exc)})
                raise

        return wrapper

    return deco
