from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import UUID
from apps.backend.app.modules.educacao.domain.enums import StatusFluxo, TipoInscricao

@dataclass
class InscricaoSuperior:
    id: UUID
    numero_processo: str
    citizen_id: UUID
    escola_id: UUID
    data_inscricao: date
    status: StatusFluxo = StatusFluxo.PENDENTE
    tipo: TipoInscricao = TipoInscricao.SUPERIOR
    observacoes: Optional[str] = None

    def confirmar(self) -> None:
        if self.status != StatusFluxo.PENDENTE:
            raise ValueError('Apenas inscricoes pendentes podem ser confirmadas')
        self.status = StatusFluxo.CONFIRMADA

    def cancelar(self, motivo: str) -> None:
        if self.status in {StatusFluxo.CONCLUIDA, StatusFluxo.CANCELADA}:
            raise ValueError(f'Inscricao ja esta {self.status.value}')
        self.status = StatusFluxo.CANCELADA
        self.observacoes = motivo