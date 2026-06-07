from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class QuotaCreate(BaseModel):
    especie_id: UUID
    zona_pesca_id: UUID
    limite_kg: Decimal


class QuotaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    especie_id: UUID
    zona_pesca_id: UUID
    ano: int
    limite_kg: Decimal
    utilizado_kg: Decimal
