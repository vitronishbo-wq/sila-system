from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.society.emprego.domain.enums import (
    Escolaridade,
    SituacaoProfissional,
    StatusCandidato,
)


class CandidatoCreate(BaseModel):
    citizen_id: UUID
    escolaridade: Escolaridade
    situacao: SituacaoProfissional
    areas_interesse: list[str] = Field(..., min_length=1)


class CandidatoUpdate(BaseModel):
    escolaridade: Escolaridade | None = None
    situacao: SituacaoProfissional | None = None
    areas_interesse: list[str] | None = None


class CandidatoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_processo: str
    citizen_id: UUID
    data_registro: date
    escolaridade: Escolaridade
    situacao: SituacaoProfissional
    areas_interesse: list[str]
    status: StatusCandidato
    observacoes: str | None = None


class CandidatoFilter(BaseModel):
    escolaridade: Escolaridade | None = None
    situacao: SituacaoProfissional | None = None
    area_interesse: str | None = None


class CandidatoDeactivate(BaseModel):
    actor_id: UUID
    motivo: str = Field(default="Desativado manualmente", min_length=3, max_length=500)
