from __future__ import annotations

from ...domain.repositories.audit_log_repository import AuditLogRepository


class AuditLogRepositoryImpl(AuditLogRepository):
    def __init__(self):
        self._events = []

    def save(self, event):
        self._events.append(event)
        return event

    def list(self):
        return list(self._events)
