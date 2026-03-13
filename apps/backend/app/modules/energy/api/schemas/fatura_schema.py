from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.energy.domain.enums import BandeiraTarifaria, StatusFaturaEnergia

class FaturaGerarPorConsumoInput(BaseModel):
    consumo_id: UUID
    data_referencia: date | None = None

class FaturaPagamentoInput(BaseModel):
    data_pagamento: date
    valor_pago: Decimal
    metodo_pagamento: str

class FaturaEnergiaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
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
