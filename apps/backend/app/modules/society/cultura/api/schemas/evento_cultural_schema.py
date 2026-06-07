from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.society.cultura.domain.enums import (
    StatusEventoCultural,
    TipoEventoCultural,
)


class EventoCulturalCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    tipo: TipoEventoCultural
    descricao: str = Field(..., min_length=5)
    data_inicio: date
    data_fim: date
    local: str = Field(..., min_length=3)
    municipio: str = Field(..., min_length=2)
    provincia: str = Field(..., min_length=2)
    realizador_id: UUID
    atracao_turistica_id: UUID | None = None
    instituicao_educacional_id: UUID | None = None
    entrada_gratuita: bool = True
    valor_ingresso: Decimal | None = None
    publico_estimado: int | None = Field(default=None, ge=0)
    observacoes: str | None = None


class EventoCulturalUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=3)
    tipo: TipoEventoCultural | None = None
    descricao: str | None = Field(default=None, min_length=5)
    data_inicio: date | None = None
    data_fim: date | None = None
    local: str | None = Field(default=None, min_length=3)
    municipio: str | None = Field(default=None, min_length=2)
    provincia: str | None = Field(default=None, min_length=2)
    atracao_turistica_id: UUID | None = None
    instituicao_educacional_id: UUID | None = None
    entrada_gratuita: bool | None = None
    valor_ingresso: Decimal | None = Field(default=None, ge=0)
    publico_estimado: int | None = Field(default=None, ge=0)
    status: StatusEventoCultural | None = None
    ativo: bool | None = None
    observacoes: str | None = None


class EventoCulturalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_evento: str
    nome: str
    tipo: TipoEventoCultural
    descricao: str
    data_inicio: date
    data_fim: date
    local: str
    municipio: str
    provincia: str
    realizador_id: UUID
    data_cadastro: date
    status: StatusEventoCultural
    atracao_turistica_id: UUID | None = None
    instituicao_educacional_id: UUID | None = None
    entrada_gratuita: bool
    valor_ingresso: Decimal | None = None
    publico_estimado: int | None = None
    ativo: bool
    observacoes: str | None = None
