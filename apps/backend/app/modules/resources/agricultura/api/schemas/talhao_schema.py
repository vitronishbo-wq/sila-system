from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusTalhao

class TalhaoCreate(BaseModel):
    codigo_propriedade: str
    nome: str
    area_ha: float
    tipo_solo: str | None = None
    irrigado: bool = False

class TalhaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_talhao: str
    codigo_propriedade: str
    nome: str
    area_ha: float
    tipo_solo: str | None
    irrigado: bool
    status: StatusTalhao
    data_cadastro: date