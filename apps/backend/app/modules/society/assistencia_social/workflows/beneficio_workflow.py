from __future__ import annotations

from sila_platform.governance.audit.logger import AuditLogger, AuditAction
from sila_platform.governance.workflows.engine import (
    WorkflowEngine,
    WorkflowInstance,
    WorkflowStep,
    WorkflowStatus,
)


BENEFICIO_STEPS = [
    WorkflowStep(name="pedido", actor_type="citizen", order=0),
    WorkflowStep(name="verificacao_nif", actor_type="admin", order=1),
    WorkflowStep(name="verificacao_ss", actor_type="admin", order=2),
    WorkflowStep(name="aprovado", actor_type="system", order=3),
]


class BeneficioWorkflowEngine:
    """Thin workflow adapter for beneficio_social."""

    def __init__(self) -> None:
        self._gov = WorkflowEngine()
        # keep a lightweight in-memory map of last published event ids per provider
        # This is intentionally local to the module wrapper to avoid touching
        # the global Governance implementation while still enabling causation_id
        # propagation inside this process's handlers.
        self._last_event: dict[str, str | None] = {}

    def criar(self, provider: str, beneficiario_id: str, metadata: dict | None = None) -> WorkflowInstance:
        meta = {"beneficiario_id": beneficiario_id, **(metadata or {})}
        inst = self._gov.create(provider, "beneficio", BENEFICIO_STEPS, meta)
        # initialize last-event tracking
        self._last_event[provider] = None
        return inst

    def set_last_event(self, provider: str, event_id: str | None) -> None:
        self._last_event[provider] = event_id

    def get_last_event(self, provider: str) -> str | None:
        return self._last_event.get(provider)

    def avancar(self, provider: str, actor: str, audit_logger: AuditLogger | None = None) -> WorkflowInstance:
        result = self._gov.advance(provider, actor)
        if audit_logger:
            audit_logger.log(
                actor_id="",
                actor_role=actor,
                action=AuditAction.UPDATE,
                resource_type="beneficio_workflow",
                resource_id=provider,
                module="assistencia_social",
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
                resource_type="beneficio_workflow",
                resource_id=provider,
                module="assistencia_social",
                details={"status": result.status.value},
            )
        return result

    def get(self, provider: str) -> WorkflowInstance | None:
        return self._gov.get(provider)

