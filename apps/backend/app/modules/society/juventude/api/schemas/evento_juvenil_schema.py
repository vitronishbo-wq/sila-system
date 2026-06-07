from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.society.juventude.domain.enums import (
    AreaInteresse,
    StatusEvento,
    TipoEvento,
)


class EventoJuvenilCreate(BaseModel):
    titulo: str = Field(..., min_length=3)
    tipo_evento: TipoEvento
    area_interesse: AreaInteresse
    data_evento: date
    local: str = Field(..., min_length=3)
    municipio: str
    provincia: str
    vagas: int | None = Field(default=None, gt=0)
    observacoes: str | None = None


class EventoJuvenilInscricao(BaseModel):
    jovem_id: UUID


class EventoJuvenilResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_evento: str
    titulo: str
    tipo_evento: TipoEvento
    area_interesse: AreaInteresse
    data_evento: date
    local: str
    municipio: str
    provincia: str
    vagas: int | None = None
    participantes: list[UUID] | None = None
    status: StatusEvento
    data_cadastro: date
    observacoes: str | None = None
    ativo: bool
