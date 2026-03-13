from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.society.cultura.domain.enums import StatusTombamento, TipoPatrimonio

class BemCulturalCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    tipo: TipoPatrimonio
    descricao: str = Field(..., min_length=5)
    localizacao: str = Field(..., min_length=3)
    municipio: str = Field(..., min_length=2)
    provincia: str = Field(..., min_length=2)
    coordenadas_lat: Decimal | None = None
    coordenadas_long: Decimal | None = None
    observacoes: str | None = None

class BemCulturalUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=3)
    tipo: TipoPatrimonio | None = None
    descricao: str | None = Field(default=None, min_length=5)
    localizacao: str | None = Field(default=None, min_length=3)
    municipio: str | None = Field(default=None, min_length=2)
    provincia: str | None = Field(default=None, min_length=2)
    coordenadas_lat: Decimal | None = None
    coordenadas_long: Decimal | None = None
    ativo: bool | None = None
    observacoes: str | None = None

class BemCulturalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    registro_ipat: str
    nome: str
    tipo: TipoPatrimonio
    descricao: str
    localizacao: str
    municipio: str
    provincia: str
    data_cadastro: date
    status_tombamento: StatusTombamento
    coordenadas_lat: Decimal | None = None
    coordenadas_long: Decimal | None = None
    tombamento_id: UUID | None = None
    ativo: bool
    observacoes: str | None = None