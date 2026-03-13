from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.resources.agricultura.domain.enums import StatusCredito

class CreditoCreate(BaseModel):
    codigo_produtor: str
    finalidade: str
    valor_solicitado: float

class CreditoAprovacaoInput(BaseModel):
    valor_aprovado: float

class CreditoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_credito: str
    codigo_produtor: str
    finalidade: str
    valor_solicitado: float
    valor_aprovado: float | None = None
    status: StatusCredito
    data_solicitacao: date
    data_aprovacao: date | None = None
    data_desembolso: date | None = None