from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.society.emprego.domain.enums import (
    Escolaridade,
    SituacaoProfissional,
    StatusCandidato,
)


@dataclass
class Candidato:
    id: UUID
    numero_processo: str
    citizen_id: UUID
    data_registro: date
    escolaridade: Escolaridade
    situacao: SituacaoProfissional
    areas_interesse: list[str]
    experiencias: list[dict] | None = None
    habilidades: list[str] | None = None
    status: StatusCandidato = StatusCandidato.ATIVO
    observacoes: str | None = None

    @classmethod
    def criar(
        cls,
        *,
        citizen_id: UUID,
        escolaridade: Escolaridade,
        situacao: SituacaoProfissional,
        areas_interesse: list[str],
        numero_processo: str,
    ) -> Candidato:
        return cls(
            id=uuid4(),
            numero_processo=numero_processo,
            citizen_id=citizen_id,
            data_registro=date.today(),
            escolaridade=escolaridade,
            situacao=situacao,
            areas_interesse=areas_interesse,
            status=StatusCandidato.ATIVO,
        )

    def atualizar_dados(
        self,
        *,
        escolaridade: Escolaridade | None = None,
        situacao: SituacaoProfissional | None = None,
        areas_interesse: list[str] | None = None,
    ) -> None:
        if escolaridade is not None:
            self.escolaridade = escolaridade
        if situacao is not None:
            self.situacao = situacao
        if areas_interesse is not None:
            self.areas_interesse = areas_interesse

    def desativar(self, motivo: str) -> None:
        self.status = StatusCandidato.INATIVO
        self.observacoes = motivo
