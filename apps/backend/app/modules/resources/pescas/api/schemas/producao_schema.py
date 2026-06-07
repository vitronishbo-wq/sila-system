from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProducaoCreate(BaseModel):
    data_producao: date
    quantidade_kg: Decimal
    unidade_processamento: str
    destino: str


class ProducaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    data_producao: date
    quantidade_kg: Decimal
    unidade_processamento: str
    destino: str
    observacoes: str | None = None
