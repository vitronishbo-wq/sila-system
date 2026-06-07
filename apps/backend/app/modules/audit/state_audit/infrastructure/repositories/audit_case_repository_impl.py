from __future__ import annotations

from ...domain.entities.audit_case import AuditCase
from ...domain.repositories.audit_case_repository import AuditCaseRepository


class AuditCaseRepositoryImpl(AuditCaseRepository):
    def __init__(self):
        self._cases = []

    def open_case(self, alert):
        case = AuditCase(
            title=f"Audit Case: {alert.rule_triggered}",
            description=alert.description,
            entity_id=alert.entity_id,
        )
        self._cases.append(case)
        return case

    def list_cases(self):
        return list(self._cases)
