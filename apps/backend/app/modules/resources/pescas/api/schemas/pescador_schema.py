from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.resources.pescas.domain.enums import TipoPescador


class PescadorCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    tipo: TipoPescador
    citizen_id: UUID
    numero_registro: str | None = None


class PescadorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    nome: str
    numero_registro: str
    tipo: TipoPescador
    citizen_id: UUID
    ativo: bool


class PescadorFilter(BaseModel):
    tipo: TipoPescador | None = None
