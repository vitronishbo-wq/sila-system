from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4
from apps.backend.app.modules.society.seguranca_social.domain.enums import Periodicidade, StatusPensao, TipoPensao

@dataclass
class Pensao:
    id: UUID
    numero_processo: str
    beneficiario_id: UUID
    tipo: TipoPensao
    data_inicio: date
    valor_mensal: Decimal
    periodicidade: Periodicidade
    status: StatusPensao
    data_fim: Optional[date] = None
    conta_bancaria: Optional[str] = None
    iban: Optional[str] = None
    observacoes: Optional[str] = None

    @classmethod
    def solicitar(cls, *, beneficiario_id: UUID, tipo: TipoPensao, valor_mensal: Decimal, numero_processo: str, conta_bancaria: Optional[str]=None, iban: Optional[str]=None) -> 'Pensao':
        return cls(id=uuid4(), numero_processo=numero_processo, beneficiario_id=beneficiario_id, tipo=tipo, data_inicio=date.today(), valor_mensal=valor_mensal, periodicidade=Periodicidade.MENSAL, status=StatusPensao.AGUARDANDO_APROVACAO, conta_bancaria=conta_bancaria, iban=iban)

    def aprovar(self) -> None:
        if self.status != StatusPensao.AGUARDANDO_APROVACAO:
            raise ValueError('Pensao nao esta aguardando aprovacao')
        self.status = StatusPensao.ATIVA

    def suspender(self, motivo: str) -> None:
        if self.status != StatusPensao.ATIVA:
            raise ValueError('Apenas pensoes ativas podem ser suspensas')
        self.status = StatusPensao.SUSPENSA
        self.observacoes = motivo

    def cancelar(self, motivo: str) -> None:
        if self.status == StatusPensao.CANCELADA:
            raise ValueError('Pensao ja esta cancelada')
        self.status = StatusPensao.CANCELADA
        self.observacoes = motivo
        self.data_fim = date.today()