from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from apps.backend.app.modules.society.assistencia_social.domain.enums import StatusCadastroUnico


@dataclass
class CadastroUnico:
    id: UUID
    codigo: str
    citizen_id_responsavel: UUID
    renda_per_capita: Decimal
    composicao_familiar: list[dict]
    condicoes_moradia: str
    acesso_agua: bool
    acesso_energia: bool
    status: StatusCadastroUnico
    data_cadastro: date
    observacoes: str | None = None

    @classmethod
    def registrar(
        cls,
        *,
        codigo: str,
        citizen_id_responsavel: UUID,
        renda_per_capita: Decimal,
        composicao_familiar: list[dict],
        condicoes_moradia: str,
        acesso_agua: bool,
        acesso_energia: bool,
        observacoes: str | None = None,
    ) -> CadastroUnico:
        return cls(
            id=uuid4(),
            codigo=codigo,
            citizen_id_responsavel=citizen_id_responsavel,
            renda_per_capita=renda_per_capita,
            composicao_familiar=composicao_familiar,
            condicoes_moradia=condicoes_moradia,
            acesso_agua=acesso_agua,
            acesso_energia=acesso_energia,
            status=StatusCadastroUnico.ATIVO,
            data_cadastro=date.today(),
            observacoes=observacoes,
        )

    def calcular_programas_elegiveis(self) -> list[str]:
        elegiveis: list[str] = []
        if self.renda_per_capita < Decimal("100"):
            elegiveis.append("BOLSA_FAMILIA")
        if any(int(item.get("idade", 0)) < 6 for item in self.composicao_familiar):
            elegiveis.append("AUXILIO_NUTRICIONAL")
        if any(int(item.get("idade", 0)) >= 65 for item in self.composicao_familiar):
            elegiveis.append("BPC_IDOSO")
        return elegiveis

    def inativar(self, motivo: str | None = None) -> None:
        self.status = StatusCadastroUnico.INATIVO
        if motivo:
            self.observacoes = motivo
