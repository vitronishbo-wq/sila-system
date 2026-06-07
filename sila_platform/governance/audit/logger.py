from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class AuditAction(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    DELEGATE = "delegate"
    REVOKE = "revoke"
    APPROVE = "approve"
    REJECT = "reject"
    SIGN = "sign"
    LOGIN = "login"
    LOGOUT = "logout"
    EXPORT = "export"
    CANCEL = "cancel"


@dataclass
class AuditEntry:
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    actor_id: str = ""
    actor_role: str = ""
    action: AuditAction = AuditAction.READ
    resource_type: str = ""
    resource_id: str = ""
    module: str = ""
    details: Optional[dict] = None
    ip_address: Optional[str] = None
    success: bool = True


class AuditLogger:
    """Trilha de auditoria comum a todos os módulos governamentais."""

    def __init__(self) -> None:
        self._entries: list[AuditEntry] = []

    def log(
        self,
        actor_id: str,
        actor_role: str,
        action: AuditAction,
        resource_type: str,
        resource_id: str,
        module: str,
        details: Optional[dict] = None,
        ip_address: Optional[str] = None,
        success: bool = True,
    ) -> AuditEntry:
        entry = AuditEntry(
            actor_id=actor_id,
            actor_role=actor_role,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            module=module,
            details=details,
            ip_address=ip_address,
            success=success,
        )
        self._entries.append(entry)
        return entry

    def query(
        self,
        module: Optional[str] = None,
        actor_id: Optional[str] = None,
        action: Optional[AuditAction] = None,
        resource_type: Optional[str] = None,
        limit: int = 100,
    ) -> list[AuditEntry]:
        results = self._entries
        if module:
            results = [e for e in results if e.module == module]
        if actor_id:
            results = [e for e in results if e.actor_id == actor_id]
        if action:
            results = [e for e in results if e.action == action]
        if resource_type:
            results = [e for e in results if e.resource_type == resource_type]
        return results[-limit:]

    def count_by_module(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for e in self._entries:
            counts[e.module] = counts.get(e.module, 0) + 1
        return counts
