from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.society.assistencia_social.domain.enums import PublicoAlvo, StatusProgramaSocial

@dataclass
class ProgramaSocial:
    id: UUID
    codigo: str
    nome: str
    publico_alvo: PublicoAlvo
    criterio_renda_max: Decimal
    valor_base: Decimal
    vagas: int | None
    status: StatusProgramaSocial
    data_inicio: date
    data_fim: date | None = None
    observacoes: str | None = None

    @classmethod
    def criar(cls, *, codigo: str, nome: str, publico_alvo: PublicoAlvo, criterio_renda_max: Decimal, valor_base: Decimal, vagas: int | None, data_inicio: date, observacoes: str | None=None) -> 'ProgramaSocial':
        return cls(id=uuid4(), codigo=codigo, nome=nome, publico_alvo=publico_alvo, criterio_renda_max=criterio_renda_max, valor_base=valor_base, vagas=vagas, status=StatusProgramaSocial.RASCUNHO, data_inicio=data_inicio, observacoes=observacoes)

    def ativar(self) -> None:
        self.status = StatusProgramaSocial.ATIVO

    def suspender(self, motivo: str | None=None) -> None:
        self.status = StatusProgramaSocial.SUSPENSO
        if motivo:
            self.observacoes = motivo

    def encerrar(self, data_fim: date, motivo: str | None=None) -> None:
        self.status = StatusProgramaSocial.ENCERRADO
        self.data_fim = data_fim
        if motivo:
            self.observacoes = motivo