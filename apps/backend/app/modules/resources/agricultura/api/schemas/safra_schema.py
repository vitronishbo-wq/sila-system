from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusSafra

class SafraCreate(BaseModel):
    codigo_propriedade: str
    codigo_cultura: str
    ano: int
    area_plantada_ha: float
    producao_estimada_ton: float

class ColheitaInput(BaseModel):
    producao_real_ton: float

class SafraResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_safra: str
    propriedade_id: UUID
    cultura_id: UUID
    ano: int
    area_plantada_ha: float
    producao_estimada_ton: float
    status: StatusSafra
    data_inicio: date | None = None
    data_colheita: date | None = None
    producao_real_ton: float | None = None