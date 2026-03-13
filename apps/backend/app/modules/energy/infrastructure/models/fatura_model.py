from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID
from app.modules.energy.domain.enums import BandeiraTarifaria, StatusFaturaEnergia

@dataclass
class FaturaEnergiaModel:
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
    status: StatusFaturaEnergia
    data_pagamento: date | None = None
    valor_pago: Decimal | None = None
    metodo_pagamento: str | None = None
