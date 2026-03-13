from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.modules.logistics.domain.enums import StatusReconciliacaoFinanceira, TipoTarifa

class BilhetagemEventoCreate(BaseModel):
    codigo_bilhete: str
    viagem_id: UUID
    tipo_tarifa: TipoTarifa
    valor_pago: Decimal
    forma_pagamento: str
    metadata: dict = Field(default_factory=dict)

class BilhetagemReconciliacaoInput(BaseModel):
    confirmado: bool
    referencia_externa: str | None = None

class BilhetagemEventoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_bilhete: str
    viagem_id: UUID
    tipo_tarifa: TipoTarifa
    valor_pago: Decimal
    forma_pagamento: str
    data_evento: datetime
    status_reconciliacao: StatusReconciliacaoFinanceira
    lancamento_financeiro_id: str | None = None
    referencia_externa: str | None = None
    metadata: dict = Field(default_factory=dict)
