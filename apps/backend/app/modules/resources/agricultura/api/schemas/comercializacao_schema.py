from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ComercializacaoCreate(BaseModel):
    codigo_safra: str
    comprador: str
    quantidade_ton: float
    preco_unitario: float


class ComercializacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_comercializacao: str
    codigo_safra: str
    comprador: str
    quantidade_ton: float
    preco_unitario: float
    valor_total: float
    data_venda: date
