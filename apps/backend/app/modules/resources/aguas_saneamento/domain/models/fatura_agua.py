from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from app.modules.resources.aguas_saneamento.domain.enums import MetodoPagamento, StatusFatura

@dataclass
class FaturaAgua:
    id: UUID
    numero_fatura: str
    consumo_id: UUID
    titular_id: UUID
    referencia: str
    volume_m3: Decimal
    tarifa_m3: Decimal
    valor_total: Decimal
    status: StatusFatura
    data_emissao: date
    data_vencimento: date
    data_pagamento: date | None = None
    valor_pago: Decimal | None = None
    metodo_pagamento: MetodoPagamento | None = None
    observacoes: str | None = None

    @classmethod
    def emitir(cls, *, consumo_id: UUID, titular_id: UUID, referencia: str, volume_m3: Decimal, tarifa_m3: Decimal, data_vencimento: date) -> 'FaturaAgua':
        if len(referencia) != 7 or referencia[4] != '-':
            raise ValueError('Referencia deve seguir formato YYYY-MM')
        if volume_m3 <= Decimal('0'):
            raise ValueError('Volume faturado deve ser maior que zero')
        if tarifa_m3 <= Decimal('0'):
            raise ValueError('Tarifa por m3 deve ser maior que zero')
        if data_vencimento <= date.today():
            raise ValueError('Data de vencimento deve ser futura')
        valor_total = (volume_m3 * tarifa_m3).quantize(Decimal('0.01'))
        return cls(id=uuid4(), numero_fatura='', consumo_id=consumo_id, titular_id=titular_id, referencia=referencia, volume_m3=volume_m3.quantize(Decimal('0.01')), tarifa_m3=tarifa_m3.quantize(Decimal('0.01')), valor_total=valor_total, status=StatusFatura.EMITIDA, data_emissao=date.today(), data_vencimento=data_vencimento)

    def registrar_pagamento(self, *, data_pagamento: date, valor_pago: Decimal, metodo_pagamento: MetodoPagamento) -> None:
        if self.status == StatusFatura.CANCELADA:
            raise ValueError('Fatura cancelada nao pode ser paga')
        if self.status == StatusFatura.PAGA:
            raise ValueError('Fatura ja paga')
        if valor_pago <= Decimal('0'):
            raise ValueError('Valor pago deve ser maior que zero')
        if valor_pago < self.valor_total:
            raise ValueError('Valor pago nao pode ser menor que valor total')
        if data_pagamento < self.data_emissao:
            raise ValueError('Data de pagamento invalida')
        self.status = StatusFatura.PAGA
        self.data_pagamento = data_pagamento
        self.valor_pago = valor_pago.quantize(Decimal('0.01'))
        self.metodo_pagamento = metodo_pagamento
        self.observacoes = None

    def cancelar(self, motivo: str) -> None:
        if self.status == StatusFatura.PAGA:
            raise ValueError('Fatura paga nao pode ser cancelada')
        if self.status == StatusFatura.CANCELADA:
            raise ValueError('Fatura ja cancelada')
        if not motivo.strip():
            raise ValueError('Motivo do cancelamento e obrigatorio')
        self.status = StatusFatura.CANCELADA
        self.observacoes = motivo.strip()

    def atualizar_status_vencimento(self) -> None:
        if self.status == StatusFatura.EMITIDA and date.today() > self.data_vencimento:
            self.status = StatusFatura.VENCIDA