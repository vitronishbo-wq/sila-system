from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class OrchestrationStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class StepCall:
    order: int
    module: str
    service_id: str
    input: dict[str, Any] = field(default_factory=dict)
    output: Optional[dict] = None
    status: OrchestrationStatus = OrchestrationStatus.PENDING
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


@dataclass
class Orchestration:
    """Orquestração de um workflow cross-sector.
    
    Exemplo: ConstituirEmpresa chama Justiça → Finanças → Admin Local → SegSocial
    """
    id: str
    workflow_name: str
    initiator_module: str
    citizen_id: str
    steps: list[StepCall] = field(default_factory=list)
    status: OrchestrationStatus = OrchestrationStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    concluded_at: Optional[datetime] = None
    metadata: dict[str, Any] = field(default_factory=dict)


class WorkflowOrchestrator:
    """Orquestrador de workflows que atravessam múltiplos módulos."""

    def __init__(self) -> None:
        self._orchestrations: dict[str, Orchestration] = {}

    def create(self, wf_name: str, initiator: str, citizen_id: str,
               steps: list[dict], metadata: Optional[dict] = None) -> Orchestration:
        """steps: [{"module": "justica", "service_id": "validar_socios", "input": {...}}, ...]"""
        step_calls = [
            StepCall(order=i, **s)
            for i, s in enumerate(steps)
        ]
        orch = Orchestration(
            id=f"{wf_name}-{citizen_id}-{datetime.now(timezone.utc).timestamp()}",
            workflow_name=wf_name, initiator_module=initiator,
            citizen_id=citizen_id, steps=step_calls,
            status=OrchestrationStatus.RUNNING, metadata=metadata or {},
        )
        self._orchestrations[orch.id] = orch
        return orch

    def complete_step(self, orch_id: str, step_order: int, output: dict) -> Optional[Orchestration]:
        orch = self._orchestrations.get(orch_id)
        if not orch:
            return None
        for step in orch.steps:
            if step.order == step_order:
                step.status = OrchestrationStatus.COMPLETED
                step.output = output
                step.completed_at = datetime.now(timezone.utc)
                break
        if all(s.status == OrchestrationStatus.COMPLETED for s in orch.steps):
            orch.status = OrchestrationStatus.COMPLETED
            orch.concluded_at = datetime.now(timezone.utc)
        return orch

    def fail_step(self, orch_id: str, step_order: int, error: str) -> Optional[Orchestration]:
        orch = self._orchestrations.get(orch_id)
        if not orch:
            return None
        for step in orch.steps:
            if step.order == step_order:
                step.status = OrchestrationStatus.FAILED
                step.error = error
                step.completed_at = datetime.now(timezone.utc)
                break
        orch.status = OrchestrationStatus.FAILED
        orch.concluded_at = datetime.now(timezone.utc)
        return orch

    def get(self, orch_id: str) -> Optional[Orchestration]:
        return self._orchestrations.get(orch_id)

    def list_by_citizen(self, citizen_id: str) -> list[Orchestration]:
        return [o for o in self._orchestrations.values() if o.citizen_id == citizen_id]

    def list_running(self) -> list[Orchestration]:
        return [o for o in self._orchestrations.values() if o.status == OrchestrationStatus.RUNNING]
