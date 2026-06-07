from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any
from uuid import UUID

from apps.backend.app.modules.educacao.domain.enums import StatusFluxo


@dataclass
class WorkflowRecord:
    id: UUID
    numero_processo: str
    service_type: str
    citizen_id: UUID
    instituicao_id: UUID
    data_registo: date
    status: StatusFluxo = StatusFluxo.PENDENTE
    observacoes: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def confirmar(self) -> None:
        if self.status != StatusFluxo.PENDENTE:
            raise ValueError("Apenas registos pendentes podem ser confirmados")
        self.status = StatusFluxo.CONFIRMADA

    def concluir(self, resumo: str | None = None) -> None:
        if self.status in {StatusFluxo.CANCELADA, StatusFluxo.CONCLUIDA}:
            raise ValueError(f"Registo ja esta {self.status.value}")
        self.status = StatusFluxo.CONCLUIDA
        if resumo:
            self.observacoes = resumo

    def cancelar(self, motivo: str) -> None:
        if self.status in {StatusFluxo.CANCELADA, StatusFluxo.CONCLUIDA}:
            raise ValueError(f"Registo ja esta {self.status.value}")
        self.status = StatusFluxo.CANCELADA
        self.observacoes = motivo
