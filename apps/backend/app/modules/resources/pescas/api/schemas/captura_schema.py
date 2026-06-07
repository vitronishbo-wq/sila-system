from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CapturaCreate(BaseModel):
    embarcacao_id: UUID
    licenca_id: UUID
    zona_pesca_id: UUID
    especie_id: UUID
    quantidade_kg: Decimal
    arte_pesca_id: UUID


class CapturaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    embarcacao_id: UUID
    licenca_id: UUID
    data_inicio: datetime
    data_fim: datetime
    zona_pesca_id: UUID
    especie_id: UUID
    quantidade_kg: Decimal
    quantidade_unidades: int | None = None
    arte_pesca_id: UUID
