from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.society.assistencia_social.domain.enums import StatusBeneficio, TipoBeneficio

@dataclass
class Beneficio:
    id: UUID
    codigo: str
    beneficiario_id: UUID
    programa_social_id: UUID | None
    tipo: TipoBeneficio
    valor: Decimal
    status: StatusBeneficio
    data_solicitacao: date
    data_concessao: date | None = None
    data_fim: date | None = None
    motivo_status: str | None = None

    @classmethod
    def solicitar(cls, *, codigo: str, beneficiario_id: UUID, tipo: TipoBeneficio, valor: Decimal, programa_social_id: UUID | None=None) -> 'Beneficio':
        return cls(id=uuid4(), codigo=codigo, beneficiario_id=beneficiario_id, programa_social_id=programa_social_id, tipo=tipo, valor=valor, status=StatusBeneficio.SOLICITADO, data_solicitacao=date.today())

    def aprovar(self, data_concessao: date | None=None) -> None:
        self.status = StatusBeneficio.APROVADO
        self.data_concessao = data_concessao or date.today()

    def negar(self, motivo: str) -> None:
        self.status = StatusBeneficio.NEGADO
        self.motivo_status = motivo

    def suspender(self, motivo: str) -> None:
        self.status = StatusBeneficio.SUSPENSO
        self.motivo_status = motivo

    def encerrar(self, motivo: str, data_fim: date | None=None) -> None:
        self.status = StatusBeneficio.ENCERRADO
        self.motivo_status = motivo
        self.data_fim = data_fim or date.today()