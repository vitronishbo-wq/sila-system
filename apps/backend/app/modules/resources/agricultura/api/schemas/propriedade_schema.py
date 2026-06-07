from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.resources.agricultura.domain.enums import TipoPropriedade


class PropriedadeCreate(BaseModel):
    produtor_id: UUID
    nome: str
    tipo: TipoPropriedade
    area_total_ha: float
    area_cultivavel_ha: float
    provincia: str | None = None
    municipio: str | None = None


class PropriedadeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_propriedade: str
    produtor_id: UUID
    nome: str
    tipo: TipoPropriedade
    area_total_ha: float
    area_cultivavel_ha: float
    provincia: str | None
    municipio: str | None
    data_cadastro: date
    ativo: bool
