from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class WorkflowStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class WorkflowStep:
    name: str
    actor_type: str
    order: int


@dataclass
class WorkflowInstance:
    provider: str
    domain_type: str
    steps: list[WorkflowStep]
    current_step: int = 0
    status: WorkflowStatus = WorkflowStatus.PENDING
    history: list[dict] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    concluded_at: Optional[datetime] = None

    def _add_history(self, step_name: str, actor: str) -> None:
        self.history.append({
            "step": step_name,
            "actor": actor,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def is_last_step(self) -> bool:
        return self.current_step >= len(self.steps) - 1


class WorkflowEngine:
    """Engine genérico de workflows governamentais.
    Reutilizável por qualquer módulo (Educação, Saúde, Justiça, etc.).
    """

    def __init__(self) -> None:
        self._instances: dict[str, WorkflowInstance] = {}

    def create(
        self,
        provider: str,
        domain_type: str,
        steps: list[WorkflowStep],
        metadata: Optional[dict] = None,
    ) -> WorkflowInstance:
        inst = WorkflowInstance(
            provider=provider,
            domain_type=domain_type,
            steps=steps,
            status=WorkflowStatus.IN_PROGRESS,
            metadata=metadata or {},
        )
        inst._add_history(steps[0].name, "sistema")
        self._instances[provider] = inst
        return inst

    def advance(self, provider: str, actor: str) -> WorkflowInstance:
        inst = self._instances.get(provider)
        if not inst:
            raise ValueError(f"Workflow {provider} nao encontrado")
        if inst.status in (WorkflowStatus.COMPLETED, WorkflowStatus.CANCELLED):
            raise ValueError(f"Workflow {provider} ja finalizado")
        if inst.is_last_step():
            raise ValueError(f"Workflow {provider} ja no estado final")
        next_idx = inst.current_step + 1
        next_step = inst.steps[next_idx]
        if actor != next_step.actor_type:
            raise PermissionError(
                f"Passo {next_step.name} requer actor={next_step.actor_type}, recebido={actor}"
            )
        inst.current_step = next_idx
        if inst.is_last_step():
            inst.status = WorkflowStatus.COMPLETED
            inst.concluded_at = datetime.now(timezone.utc)
        inst._add_history(next_step.name, actor)
        return inst

    def cancel(self, provider: str) -> WorkflowInstance:
        inst = self._instances.get(provider)
        if not inst:
            raise ValueError(f"Workflow {provider} nao encontrado")
        if inst.status in (WorkflowStatus.COMPLETED, WorkflowStatus.CANCELLED):
            raise ValueError(f"Workflow {provider} ja finalizado")
        inst.status = WorkflowStatus.CANCELLED
        inst.concluded_at = datetime.now(timezone.utc)
        inst._add_history("cancelado", "sistema")
        return inst

    def get(self, provider: str) -> Optional[WorkflowInstance]:
        return self._instances.get(provider)

    def list_by_field(self, field: str, value: str) -> list[WorkflowInstance]:
        return [
            w for w in self._instances.values()
            if w.metadata.get(field) == value
        ]
