from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.society.juventude.domain.enums import StatusInscricao


@dataclass
class InscricaoPrograma:
    id: UUID
    codigo_inscricao: str
    programa_id: UUID
    jovem_id: UUID
    data_inscricao: date
    status: StatusInscricao
    data_cadastro: date
    prioridade: int = 0
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def inscrever(
        cls,
        *,
        codigo_inscricao: str,
        programa_id: UUID,
        jovem_id: UUID,
        prioridade: int = 0,
        observacoes: str | None = None,
    ) -> InscricaoPrograma:
        if prioridade < 0:
            raise ValueError("Prioridade da inscricao nao pode ser negativa")
        return cls(
            id=uuid4(),
            codigo_inscricao=codigo_inscricao.strip(),
            programa_id=programa_id,
            jovem_id=jovem_id,
            data_inscricao=date.today(),
            status=StatusInscricao.PENDENTE,
            data_cadastro=date.today(),
            prioridade=prioridade,
            observacoes=observacoes.strip() if observacoes else None,
            ativo=True,
        )

    def confirmar(self) -> None:
        if self.status in {StatusInscricao.CANCELADA, StatusInscricao.CONCLUIDA}:
            raise ValueError(f"Inscricao ja finalizada com status {self.status.value}")
        self.status = StatusInscricao.CONFIRMADA

    def concluir(self) -> None:
        if self.status == StatusInscricao.CANCELADA:
            raise ValueError("Inscricao cancelada nao pode ser concluida")
        self.status = StatusInscricao.CONCLUIDA
        self.ativo = False

    def cancelar(self, motivo: str | None = None) -> None:
        self.status = StatusInscricao.CANCELADA
        self.ativo = False
        if motivo:
            self.observacoes = motivo.strip()
