from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.society.cultura.domain.enums import (
    CategoriaPatrimonioImaterial,
    StatusPatrimonioImaterial,
)


class PatrimonioImaterialCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    categoria: CategoriaPatrimonioImaterial
    descricao: str = Field(..., min_length=10)
    comunidade: str = Field(..., min_length=2)
    municipio: str = Field(..., min_length=2)
    provincia: str = Field(..., min_length=2)
    atracao_turistica_id: UUID | None = None
    instituicao_educacional_id: UUID | None = None
    plano_salvaguarda: str | None = None
    observacoes: str | None = None


class PatrimonioImaterialUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=3)
    categoria: CategoriaPatrimonioImaterial | None = None
    descricao: str | None = Field(default=None, min_length=10)
    comunidade: str | None = Field(default=None, min_length=2)
    municipio: str | None = Field(default=None, min_length=2)
    provincia: str | None = Field(default=None, min_length=2)
    atracao_turistica_id: UUID | None = None
    instituicao_educacional_id: UUID | None = None
    plano_salvaguarda: str | None = None
    status: StatusPatrimonioImaterial | None = None
    ativo: bool | None = None
    observacoes: str | None = None


class PatrimonioImaterialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    registro_pni: str
    nome: str
    categoria: CategoriaPatrimonioImaterial
    descricao: str
    comunidade: str
    municipio: str
    provincia: str
    data_registro: date
    status: StatusPatrimonioImaterial
    atracao_turistica_id: UUID | None = None
    instituicao_educacional_id: UUID | None = None
    plano_salvaguarda: str | None = None
    ativo: bool
    observacoes: str | None = None
