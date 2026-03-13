from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.modules.infrastructure_sector.aviacao_civil.domain.enums import FaseVoo, GravidadeOcorrencia, TipoOcorrencia

class OcorrenciaCreate(BaseModel):
    tipo: TipoOcorrencia
    voo_id: UUID | None = None
    aeronave_id: UUID
    data_ocorrencia: datetime
    local: dict
    fase_voo: FaseVoo
    descricao: str = Field(min_length=5, max_length=4000)
    vitimas: dict[str, int] = Field(default_factory=dict)
    danos: str = Field(min_length=3, max_length=64)

class OcorrenciaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_ocorrencia: str
    tipo: TipoOcorrencia
    voo_id: UUID | None
    aeronave_id: UUID
    data_ocorrencia: datetime
    data_registro: datetime
    local: dict
    fase_voo: FaseVoo
    descricao: str
    vitimas: dict[str, int]
    danos: str
    gravidade: GravidadeOcorrencia
    status: str