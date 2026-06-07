from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.society.cultura.domain.enums import TipoArtista


class ArtistaCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    tipo: list[TipoArtista]
    citizen_id: UUID | None = None
    nome_artistico: str | None = None
    data_nascimento: date | None = None
    naturalidade: str | None = None
    nacionalidade: str = "Angolana"
    biografia: str | None = None
    municipio: str | None = None
    provincia: str | None = None
    observacoes: str | None = None


class ArtistaUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=3)
    tipo: list[TipoArtista] | None = None
    nome_artistico: str | None = None
    data_nascimento: date | None = None
    naturalidade: str | None = None
    nacionalidade: str | None = None
    biografia: str | None = None
    municipio: str | None = None
    provincia: str | None = None
    ativo: bool | None = None
    observacoes: str | None = None


class ArtistaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    registro_cultural: str
    nome: str
    tipo: list[TipoArtista]
    data_cadastro: date
    nome_artistico: str | None = None
    data_nascimento: date | None = None
    naturalidade: str | None = None
    nacionalidade: str
    biografia: str | None = None
    citizen_id: UUID | None = None
    municipio: str | None = None
    provincia: str | None = None
    ativo: bool
    observacoes: str | None = None
