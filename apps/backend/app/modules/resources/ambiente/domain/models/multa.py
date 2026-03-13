from __future__ import annotations
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.resources.ambiente.domain.enums import StatusMulta

@dataclass
class Multa:
    id: UUID
    numero_multa: str
    numero_auto_infracao: str
    valor: Decimal
    status: StatusMulta
    data_aplicacao: date
    data_vencimento: date
    data_pagamento: date | None = None
    quantidade_parcelas: int | None = None
    observacoes: str | None = None

    @classmethod
    def aplicar(cls, *, numero_auto_infracao: str, valor: Decimal, dias_vencimento: int=30) -> 'Multa':
        if valor <= Decimal('0'):
            raise ValueError('Valor da multa deve ser maior que zero')
        if dias_vencimento <= 0:
            raise ValueError('Prazo de vencimento deve ser maior que zero')
        data_aplicacao = date.today()
        return cls(id=uuid4(), numero_multa='', numero_auto_infracao=numero_auto_infracao, valor=valor.quantize(Decimal('0.01')), status=StatusMulta.APLICADA, data_aplicacao=data_aplicacao, data_vencimento=data_aplicacao + timedelta(days=dias_vencimento))

    def parcelar(self, quantidade_parcelas: int) -> None:
        if self.status not in {StatusMulta.APLICADA, StatusMulta.VENCIDA}:
            raise ValueError('Multa nao pode ser parcelada neste status')
        if quantidade_parcelas < 2:
            raise ValueError('Quantidade de parcelas deve ser pelo menos 2')
        self.status = StatusMulta.PARCELADA
        self.quantidade_parcelas = quantidade_parcelas

    def registrar_pagamento(self) -> None:
        if self.status in {StatusMulta.PAGA, StatusMulta.CANCELADA}:
            raise ValueError('Multa ja encerrada')
        self.status = StatusMulta.PAGA
        self.data_pagamento = date.today()

    def cancelar(self, motivo: str) -> None:
        if self.status == StatusMulta.CANCELADA:
            raise ValueError('Multa ja cancelada')
        if not motivo.strip():
            raise ValueError('Motivo do cancelamento da multa e obrigatorio')
        self.status = StatusMulta.CANCELADA
        self.observacoes = motivo.strip()

    def atualizar_vencimento(self) -> None:
        if self.status in {StatusMulta.APLICADA, StatusMulta.PARCELADA} and date.today() > self.data_vencimento:
            self.status = StatusMulta.VENCIDA