from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusFaturaTelecom

@dataclass
class FaturaTelecom:
    id: UUID
    numero_fatura: str
    assinante_id: UUID
    referencia: str
    consumo_total_gb: Decimal
    franquia_gb: Decimal
    excedente_gb: Decimal
    valor_plano: Decimal
    valor_excedente: Decimal
    valor_total: Decimal
    data_emissao: date
    data_vencimento: date
    status: StatusFaturaTelecom
    data_pagamento: date | None = None
    valor_pago: Decimal | None = None

    @classmethod
    def gerar(cls, *, assinante_id: UUID, referencia: str, consumo_total_gb: Decimal, franquia_gb: Decimal, valor_plano: Decimal, valor_excedente: Decimal, data_vencimento: date) -> 'FaturaTelecom':
        if not referencia.strip():
            raise ValueError('Referencia obrigatoria')
        if valor_plano < Decimal('0') or valor_excedente < Decimal('0'):
            raise ValueError('Valores da fatura invalidos')
        excedente_gb = max(consumo_total_gb - franquia_gb, Decimal('0.00')).quantize(Decimal('0.01'))
        valor_total = (valor_plano + valor_excedente).quantize(Decimal('0.01'))
        return cls(id=uuid4(), numero_fatura='', assinante_id=assinante_id, referencia=referencia.strip(), consumo_total_gb=consumo_total_gb.quantize(Decimal('0.01')), franquia_gb=franquia_gb.quantize(Decimal('0.01')), excedente_gb=excedente_gb, valor_plano=valor_plano.quantize(Decimal('0.01')), valor_excedente=valor_excedente.quantize(Decimal('0.01')), valor_total=valor_total, data_emissao=date.today(), data_vencimento=data_vencimento, status=StatusFaturaTelecom.PENDENTE)

    def registrar_pagamento(self, *, data_pagamento: date, valor_pago: Decimal) -> None:
        if self.status == StatusFaturaTelecom.PAGA:
            raise ValueError('Fatura ja paga')
        if valor_pago < self.valor_total:
            raise ValueError('Valor pago insuficiente')
        self.status = StatusFaturaTelecom.PAGA
        self.data_pagamento = data_pagamento
        self.valor_pago = valor_pago.quantize(Decimal('0.01'))