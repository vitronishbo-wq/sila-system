from __future__ import annotations

from typing import Any, Optional

from sila_platform.governance.audit.logger import AuditLogger, AuditAction
from sila_platform.governance.territory.models import TerritorialScope
from sila_platform.governance.workflows.engine import (
    WorkflowEngine,
    WorkflowInstance,
    WorkflowStep,
    WorkflowStatus,
)

from apps.backend.app.modules.educacao.rbac.roles import RoleMinisterial as RoleEducacao

MATRICULA_STEPS = [
    WorkflowStep(name="criada", actor_type=RoleEducacao.ROLE_OPERADOR.value, order=0),
    WorkflowStep(name="escola_valida", actor_type=RoleEducacao.ROLE_ESCOLA.value, order=1),
    WorkflowStep(name="municipio_confirma", actor_type=RoleEducacao.ROLE_MUNICIPIO.value, order=2),
    WorkflowStep(name="provincia_audita", actor_type=RoleEducacao.ROLE_PROVINCIA.value, order=3),
    WorkflowStep(name="concluido", actor_type=RoleEducacao.ROLE_MINISTERIO.value, order=4),
]


class MatriculaWorkflowEngine:
    """Workflow de matrícula baseado no WorkflowEngine da governance.
    Steps now use RoleEducacao enum values for RBAC enforcement.
    """

    def __init__(self) -> None:
        self._gov = WorkflowEngine()

    def criar(self, provider: str, student_id: str, school_id: str,
              municipality_id: Optional[str] = None,
              province_id: Optional[str] = None,
              territory: Optional[TerritorialScope] = None,
              metadata: Optional[dict] = None) -> WorkflowInstance:
        meta = {
            "student_id": student_id,
            "school_id": school_id,
            "municipality_id": municipality_id or "",
            "province_id": province_id or "",
            "territory": territory.to_dict() if territory else {},
            **(metadata or {}),
        }
        return self._gov.create(provider, "matricula", MATRICULA_STEPS, meta)

    def avancar(self, provider: str, actor: str, audit_logger: AuditLogger | None = None) -> WorkflowInstance:
        result = self._gov.advance(provider, actor)
        if audit_logger:
            audit_logger.log(
                actor_id="",
                actor_role=actor,
                action=AuditAction.UPDATE,
                resource_type="matricula_workflow",
                resource_id=provider,
                module="educacao",
                details={"step": result.current_step, "status": result.status.value},
            )
        return result

    def cancelar(self, provider: str, actor: str = "sistema", audit_logger: AuditLogger | None = None) -> WorkflowInstance:
        result = self._gov.cancel(provider)
        if audit_logger:
            audit_logger.log(
                actor_id="",
                actor_role=actor,
                action=AuditAction.CANCEL,
                resource_type="matricula_workflow",
                resource_id=provider,
                module="educacao",
                details={"status": result.status.value},
            )
        return result

    def get(self, provider: str) -> Optional[WorkflowInstance]:
        return self._gov.get(provider)

    def list_by_school(self, school_id: str) -> list[WorkflowInstance]:
        return self._gov.list_by_field("school_id", school_id)

    def list_by_municipality(self, municipality_id: str) -> list[WorkflowInstance]:
        return self._gov.list_by_field("municipality_id", municipality_id)
