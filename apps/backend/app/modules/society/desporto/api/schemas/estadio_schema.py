from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.society.desporto.domain.enums import EstadoRelvado, TipoEstadio


class EstadioCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    tipo: TipoEstadio
    municipio: str
    provincia: str
    capacidade: int = Field(..., gt=0)
    estado_relvado: EstadoRelvado
    codigo_obra_instalacao: str | None = None
    clube_mandante_id: UUID | None = None
    observacoes: str | None = None


class EstadioUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=3)
    tipo: TipoEstadio | None = None
    municipio: str | None = None
    provincia: str | None = None
    capacidade: int | None = Field(default=None, gt=0)
    estado_relvado: EstadoRelvado | None = None
    codigo_obra_instalacao: str | None = None
    clube_mandante_id: UUID | None = None
    ativo: bool | None = None
    observacoes: str | None = None


class EstadioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_estadio: str
    nome: str
    tipo: TipoEstadio
    municipio: str
    provincia: str
    capacidade: int
    estado_relvado: EstadoRelvado
    data_cadastro: date
    codigo_obra_instalacao: str | None = None
    clube_mandante_id: UUID | None = None
    ativo: bool
    observacoes: str | None = None
