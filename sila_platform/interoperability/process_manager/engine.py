from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class ProcessStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"


@dataclass
class ProcessStep:
    name: str
    module: str
    action: str
    status: ProcessStatus = ProcessStatus.ACTIVE
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[dict] = None
    error: Optional[str] = None


@dataclass
class ProcessInstance:
    """Processo de longa duração que atravessa múltiplos módulos.
    
    Difere do Orchestration porque pode ser suspenso/retomado
    e inclui steps assíncronos que aguardam ação humana.
    """
    id: str
    process_name: str
    citizen_id: str
    initiator_module: str
    steps: list[ProcessStep] = field(default_factory=list)
    status: ProcessStatus = ProcessStatus.ACTIVE
    current_step: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    concluded_at: Optional[datetime] = None
    metadata: dict[str, Any] = field(default_factory=dict)


class ProcessManager:
    """Gestor de processos de longa duração com suporte a suspensão."""

    def __init__(self) -> None:
        self._processes: dict[str, ProcessInstance] = {}

    def start(self, name: str, citizen_id: str, initiator: str,
              steps: list[dict], metadata: Optional[dict] = None) -> ProcessInstance:
        proc = ProcessInstance(
            id=f"{name}-{citizen_id}-{datetime.now(timezone.utc).timestamp()}",
            process_name=name, citizen_id=citizen_id,
            initiator_module=initiator, metadata=metadata or {},
        )
        for i, s in enumerate(steps):
            proc.steps.append(ProcessStep(
                name=s.get("name", f"step_{i}"),
                module=s.get("module", ""),
                action=s.get("action", ""),
            ))
        self._processes[proc.id] = proc
        return proc

    def advance(self, proc_id: str, result: Optional[dict] = None) -> Optional[ProcessInstance]:
        proc = self._processes.get(proc_id)
        if not proc or proc.status != ProcessStatus.ACTIVE:
            return None
        step = proc.steps[proc.current_step]
        step.status = ProcessStatus.COMPLETED
        step.result = result
        step.completed_at = datetime.now(timezone.utc)
        proc.current_step += 1
        if proc.current_step >= len(proc.steps):
            proc.status = ProcessStatus.COMPLETED
            proc.concluded_at = datetime.now(timezone.utc)
        return proc

    def suspend(self, proc_id: str) -> bool:
        proc = self._processes.get(proc_id)
        if proc and proc.status == ProcessStatus.ACTIVE:
            proc.status = ProcessStatus.SUSPENDED
            return True
        return False

    def resume(self, proc_id: str) -> bool:
        proc = self._processes.get(proc_id)
        if proc and proc.status == ProcessStatus.SUSPENDED:
            proc.status = ProcessStatus.ACTIVE
            return True
        return False

    def cancel(self, proc_id: str) -> bool:
        proc = self._processes.get(proc_id)
        if proc and proc.status in (ProcessStatus.ACTIVE, ProcessStatus.SUSPENDED):
            proc.status = ProcessStatus.CANCELLED
            proc.concluded_at = datetime.now(timezone.utc)
            return True
        return False

    def get(self, proc_id: str) -> Optional[ProcessInstance]:
        return self._processes.get(proc_id)

    def list_by_citizen(self, citizen_id: str) -> list[ProcessInstance]:
        return [p for p in self._processes.values() if p.citizen_id == citizen_id]

    def count_by_status(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for p in self._processes.values():
            counts[p.status.value] = counts.get(p.status.value, 0) + 1
        return counts
