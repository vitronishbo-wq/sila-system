from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.energy.domain.enums import BandeiraTarifaria, StatusFaturaEnergia

@dataclass
class FaturaEnergia:
    id: UUID
    numero_fatura: str
    consumo_id: UUID
    unidade_consumidora_id: UUID
    cpf_titular: str
    mes_referencia: str
    consumo_kwh: Decimal
    tarifa_kwh: Decimal
    bandeira_tarifaria: BandeiraTarifaria
    valor_consumo: Decimal
    valor_bandeira: Decimal
    valor_iluminacao_publica: Decimal
    valor_total: Decimal
    data_emissao: date
    data_vencimento: date
    status: StatusFaturaEnergia = StatusFaturaEnergia.PENDENTE
    data_pagamento: date | None = None
    valor_pago: Decimal | None = None
    metodo_pagamento: str | None = None

    @classmethod
    def gerar(cls, *, consumo_id: UUID, unidade_consumidora_id: UUID, cpf_titular: str, mes_referencia: str, consumo_kwh: Decimal, tarifa_kwh: Decimal, bandeira_tarifaria: BandeiraTarifaria, data_vencimento: date) -> 'FaturaEnergia':
        if consumo_kwh < Decimal('0'):
            raise ValueError('Consumo nao pode ser negativo')
        if tarifa_kwh <= Decimal('0'):
            raise ValueError('Tarifa kWh deve ser maior que zero')
        if data_vencimento <= date.today():
            raise ValueError('Data de vencimento deve ser futura')
        valor_consumo = (consumo_kwh * tarifa_kwh).quantize(Decimal('0.01'))
        adicional_bandeira = {BandeiraTarifaria.VERDE: Decimal('0.00'), BandeiraTarifaria.AMARELA: Decimal('0.015'), BandeiraTarifaria.VERMELHA_PATAMAR_1: Decimal('0.03'), BandeiraTarifaria.VERMELHA_PATAMAR_2: Decimal('0.05'), BandeiraTarifaria.ESCASSEZ_HIDRICA: Decimal('0.10')}
        valor_bandeira = (consumo_kwh * adicional_bandeira.get(bandeira_tarifaria, Decimal('0.00'))).quantize(Decimal('0.01'))
        valor_iluminacao = (valor_consumo * Decimal('0.05')).quantize(Decimal('0.01'))
        valor_total = (valor_consumo + valor_bandeira + valor_iluminacao).quantize(Decimal('0.01'))
        return cls(id=uuid4(), numero_fatura='', consumo_id=consumo_id, unidade_consumidora_id=unidade_consumidora_id, cpf_titular=cpf_titular.strip(), mes_referencia=mes_referencia, consumo_kwh=consumo_kwh.quantize(Decimal('0.01')), tarifa_kwh=tarifa_kwh.quantize(Decimal('0.01')), bandeira_tarifaria=bandeira_tarifaria, valor_consumo=valor_consumo, valor_bandeira=valor_bandeira, valor_iluminacao_publica=valor_iluminacao, valor_total=valor_total, data_emissao=date.today(), data_vencimento=data_vencimento)

    def registrar_pagamento(self, *, data_pagamento: date, valor_pago: Decimal, metodo_pagamento: str) -> None:
        if self.status == StatusFaturaEnergia.CANCELADA:
            raise ValueError('Fatura cancelada nao pode ser paga')
        if self.status == StatusFaturaEnergia.PAGA:
            raise ValueError('Fatura ja paga')
        if valor_pago < self.valor_total:
            raise ValueError('Valor pago nao pode ser menor que o valor total')
        if not metodo_pagamento.strip():
            raise ValueError('Metodo de pagamento obrigatorio')
        self.status = StatusFaturaEnergia.PAGA
        self.data_pagamento = data_pagamento
        self.valor_pago = valor_pago.quantize(Decimal('0.01'))
        self.metodo_pagamento = metodo_pagamento.strip().lower()
