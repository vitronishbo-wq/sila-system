from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional
from uuid import UUID


class StatusMatricula(str, Enum):
    PENDENTE = "pendente"
    ATIVA = "ativa"
    TRANSFERIDA = "transferida"
    CANCELADA = "cancelada"
    CONCLUIDA = "concluida"


@dataclass
class Matricula:
    id: UUID
    numero_processo: str
    citizen_id: UUID
    escola_id: UUID
    turma_id: UUID
    ano_letivo_id: UUID
    data_matricula: date
    status: StatusMatricula
    observacoes: Optional[str] = None

    def ativar(self) -> None:
        if self.status != StatusMatricula.PENDENTE:
            raise ValueError("Apenas matriculas pendentes podem ser ativadas")
        self.status = StatusMatricula.ATIVA

    def transferir(self) -> None:
        if self.status != StatusMatricula.ATIVA:
            raise ValueError("Apenas matriculas ativas podem ser transferidas")
        self.status = StatusMatricula.TRANSFERIDA

    def cancelar(self, motivo: str) -> None:
        if self.status in {StatusMatricula.CONCLUIDA, StatusMatricula.CANCELADA}:
            raise ValueError(f"Matricula ja esta {self.status.value}")
        self.status = StatusMatricula.CANCELADA
        self.observacoes = motivo

