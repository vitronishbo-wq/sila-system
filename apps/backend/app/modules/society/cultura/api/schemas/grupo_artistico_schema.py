from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.society.cultura.domain.enums import TipoGrupoArtistico

class GrupoArtisticoCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    tipo: TipoGrupoArtistico
    lider_artista_id: UUID
    descricao: str | None = None
    data_fundacao: date | None = None
    municipio: str | None = None
    provincia: str | None = None
    instituicao_educacional_id: UUID | None = None
    membros_ids: list[UUID] | None = None
    observacoes: str | None = None

class GrupoArtisticoUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=3)
    tipo: TipoGrupoArtistico | None = None
    lider_artista_id: UUID | None = None
    descricao: str | None = None
    data_fundacao: date | None = None
    municipio: str | None = None
    provincia: str | None = None
    instituicao_educacional_id: UUID | None = None
    membros_ids: list[UUID] | None = None
    ativo: bool | None = None
    observacoes: str | None = None

class GrupoArtisticoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_grupo: str
    nome: str
    tipo: TipoGrupoArtistico
    lider_artista_id: UUID
    data_cadastro: date
    descricao: str | None = None
    data_fundacao: date | None = None
    municipio: str | None = None
    provincia: str | None = None
    instituicao_educacional_id: UUID | None = None
    membros_ids: list[UUID] | None = None
    ativo: bool
    observacoes: str | None = None