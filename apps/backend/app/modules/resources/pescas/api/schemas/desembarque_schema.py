from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DesembarqueCreate(BaseModel):
    captura_id: UUID
    porto_desembarque: str
    quantidade_kg: Decimal


class DesembarqueResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    captura_id: UUID
    porto_desembarque: str
    data_desembarque: datetime
    quantidade_kg: Decimal
    inspecao_aprovada: bool
    observacoes: str | None = None
