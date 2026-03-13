from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Optional
from uuid import UUID
from apps.backend.app.modules.society.emprego.domain.enums import WorkflowStatus

@dataclass
class WorkflowEmpregoRecord:
    id: UUID
    numero_processo: str
    citizen_id: UUID
    data_registro: date
    service_type: str
    status: WorkflowStatus = WorkflowStatus.PENDENTE
    observacoes: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def iniciar_analise(self) -> None:
        if self.status != WorkflowStatus.PENDENTE:
            raise ValueError('Apenas registos pendentes podem iniciar analise')
        self.status = WorkflowStatus.EM_ANALISE

    def aprovar(self, observacoes: str | None=None) -> None:
        if self.status in {WorkflowStatus.CONCLUIDA, WorkflowStatus.CANCELADA}:
            raise ValueError(f'Registo ja esta {self.status.value}')
        self.status = WorkflowStatus.APROVADA
        if observacoes:
            self.observacoes = observacoes

    def concluir(self, observacoes: str | None=None) -> None:
        if self.status in {WorkflowStatus.CONCLUIDA, WorkflowStatus.CANCELADA}:
            raise ValueError(f'Registo ja esta {self.status.value}')
        self.status = WorkflowStatus.CONCLUIDA
        if observacoes:
            self.observacoes = observacoes

    def cancelar(self, motivo: str) -> None:
        if self.status == WorkflowStatus.CONCLUIDA:
            raise ValueError('Registo concluido nao pode ser cancelado')
        self.status = WorkflowStatus.CANCELADA
        self.observacoes = motivo