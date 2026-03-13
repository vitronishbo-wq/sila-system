from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.resources.agricultura.domain.enums import StatusPlantio

class PlantioCreate(BaseModel):
    codigo_safra: str
    codigo_talhao: str
    area_plantada_ha: float
    quantidade_semente: float | None = None

class PlantioCancelamentoInput(BaseModel):
    motivo: str

class PlantioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_plantio: str
    codigo_safra: str
    codigo_talhao: str
    area_plantada_ha: float
    quantidade_semente: float | None = None
    data_planejamento: date
    status: StatusPlantio
    data_execucao: date | None = None
    motivo_cancelamento: str | None = None