from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import MetodoPagamento, StatusFatura

@dataclass
class FaturaModel:
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
    data_pagamento: date | None
    valor_pago: Decimal | None
    metodo_pagamento: MetodoPagamento | None