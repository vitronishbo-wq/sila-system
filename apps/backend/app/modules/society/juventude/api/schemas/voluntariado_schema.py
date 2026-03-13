from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.society.juventude.domain.enums import AreaInteresse, StatusVoluntariado

class VoluntariadoCreate(BaseModel):
    jovem_id: UUID
    organizacao: str = Field(..., min_length=3)
    causa: AreaInteresse
    carga_horaria_total: int = Field(..., gt=0)
    data_inicio: date
    data_fim: date | None = None
    observacoes: str | None = None

class VoluntariadoStatusUpdate(BaseModel):
    status: StatusVoluntariado

class VoluntariadoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_voluntariado: str
    jovem_id: UUID
    organizacao: str
    causa: AreaInteresse
    carga_horaria_total: int
    data_inicio: date
    data_fim: date | None = None
    status: StatusVoluntariado
    data_cadastro: date
    observacoes: str | None = None
    ativo: bool