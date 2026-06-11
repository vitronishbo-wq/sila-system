from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID, uuid4

from apps.backend.app.modules.governance.workflow.domain.enums import WorkflowStatus


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class WorkflowInstance:
    """Instância em execução do workflow"""

    workflow_id: UUID
    current_state_id: UUID
    entity_type: str
    entity_id: UUID
    citizen_id: UUID
    created_by: UUID
    id: UUID = field(default_factory=uuid4)
    assigned_to: UUID | None = None
    status: WorkflowStatus = WorkflowStatus.ACTIVE
    variables: dict[str, Any] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)
    started_at: datetime = field(default_factory=_utcnow)
    completed_at: datetime | None = None
    deadline: datetime | None = None
    timeout_hours: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    updated_at: datetime | None = None

    @property
    def is_active(self) -> bool:
        return self.status == WorkflowStatus.ACTIVE

    @property
    def is_completed(self) -> bool:
        return self.status == WorkflowStatus.COMPLETED

    @property
    def time_in_state(self) -> timedelta | None:
        """Tempo no estado atual"""
        now = _utcnow()
        if self.updated_at:
            return now - self.updated_at
        return now - self.started_at

    @property
    def is_overdue(self) -> bool:
        """Verifica se está atrasado"""
        if not self.deadline:
            return False
        return _utcnow() > self.deadline

    def complete(self):
        """Completa a instância"""
        self.status = WorkflowStatus.COMPLETED
        self.completed_at = _utcnow()
        self.updated_at = _utcnow()

    def terminate(self, reason: str = None):
        """Termina a instância"""
        self.status = WorkflowStatus.TERMINATED
        self.completed_at = _utcnow()
        self.updated_at = _utcnow()
        if reason:
            self.metadata["termination_reason"] = reason

    def suspend(self):
        """Suspende a instância"""
        self.status = WorkflowStatus.SUSPENDED
        self.updated_at = _utcnow()

    def resume(self):
        """Resume a instância"""
        self.status = WorkflowStatus.ACTIVE
        self.updated_at = _utcnow()

    def set_variable(self, key: str, value: Any):
        """Define variável do processo"""
        self.variables[key] = value
        self.updated_at = _utcnow()

    def get_variable(self, key: str, default: Any = None) -> Any:
        """Obtém variável do processo"""
        return self.variables.get(key, default)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "workflow_id": str(self.workflow_id),
            "current_state_id": str(self.current_state_id),
            "entity_type": self.entity_type,
            "entity_id": str(self.entity_id),
            "citizen_id": str(self.citizen_id),
            "created_by": str(self.created_by),
            "assigned_to": str(self.assigned_to) if self.assigned_to else None,
            "status": self.status.value,
            "variables": self.variables,
            "context": self.context,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "timeout_hours": self.timeout_hours,
            "metadata": self.metadata,
            "is_active": self.is_active,
            "is_overdue": self.is_overdue,
            "time_in_state_seconds": self.time_in_state.total_seconds()
            if self.time_in_state
            else 0,
        }
