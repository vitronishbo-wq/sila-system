from uuid import uuid4

from apps.backend.app.modules.audit.state_audit.application.services.audit_service import (
    AuditService,
)
from apps.backend.app.modules.audit.state_audit.domain.services.audit_engine import AuditEngine
from apps.backend.app.modules.audit.state_audit.domain.services.compliance_rules import (
    ContractOverBudgetRule,
)
from apps.backend.app.modules.audit.state_audit.infrastructure.repositories.audit_case_repository_impl import (
    AuditCaseRepositoryImpl,
)
from apps.backend.app.modules.audit.state_audit.infrastructure.repositories.audit_log_repository_impl import (
    AuditLogRepositoryImpl,
)


def test_open_case_when_contract_over_budget():
    service = AuditService(
        AuditEngine([ContractOverBudgetRule()]), AuditLogRepositoryImpl(), AuditCaseRepositoryImpl()
    )
    alerts = service.register_event(
        {
            "type": "ContractAwarded",
            "entity_id": uuid4(),
            "metadata": {"value": 130, "estimated": 100},
        }
    )
    assert len(alerts) == 1
