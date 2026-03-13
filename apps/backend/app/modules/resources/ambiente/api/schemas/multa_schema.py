from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.resources.ambiente.domain.enums import StatusMulta

class MultaCreate(BaseModel):
    numero_auto_infracao: str
    valor: Decimal
    dias_vencimento: int = 30

class MultaParcelamentoInput(BaseModel):
    quantidade_parcelas: int

class MultaCancelamentoInput(BaseModel):
    motivo: str

class MultaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
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