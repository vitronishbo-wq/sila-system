from fastapi import APIRouter

from ..application.services.audit_service import AuditService
from ..domain.services.audit_engine import AuditEngine
from ..domain.services.compliance_rules import ContractOverBudgetRule
from ..infrastructure.repositories.audit_case_repository_impl import AuditCaseRepositoryImpl
from ..infrastructure.repositories.audit_log_repository_impl import AuditLogRepositoryImpl

router = APIRouter(prefix="/audit", tags=["state_audit"])
_log_repo = AuditLogRepositoryImpl()
_case_repo = AuditCaseRepositoryImpl()
_engine = AuditEngine([ContractOverBudgetRule()])
_service = AuditService(_engine, _log_repo, _case_repo)


@router.get("/cases")
def list_cases():
    return [c.__dict__ for c in _case_repo.list_cases()]


@router.get("/alerts")
def list_alerts():
    return []


@router.post("/event")
def register_event(payload: dict):
    alerts = _service.register_event(payload)
    return {"alerts": [a.__dict__ for a in alerts]}
