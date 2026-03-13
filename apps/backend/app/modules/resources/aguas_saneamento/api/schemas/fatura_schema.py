from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import MetodoPagamento, StatusFatura

class FaturaEmitirInput(BaseModel):
    consumo_id: UUID
    titular_id: UUID
    referencia: str
    volume_m3: Decimal
    tarifa_m3: Decimal
    data_vencimento: date

class FaturaPagamentoInput(BaseModel):
    data_pagamento: date
    valor_pago: Decimal
    metodo_pagamento: MetodoPagamento

class FaturaMotivoInput(BaseModel):
    motivo: str

class FaturaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
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