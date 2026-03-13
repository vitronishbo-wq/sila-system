from __future__ import annotations
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.tourism.domain.enums import TipoAtracao

class AtracaoTuristicaCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    tipo: TipoAtracao
    descricao: str = Field(..., min_length=5)
    endereco: str
    municipio: str
    provincia: str
    horario_funcionamento: str
    acessivel: bool
    gratuita: bool = False
    capacidade_visitantes_dia: int | None = Field(default=None, gt=0)
    valor_entrada: Decimal | None = Field(default=None, ge=0)
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    observacoes: str | None = None

class AtracaoTuristicaUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=3)
    tipo: TipoAtracao | None = None
    descricao: str | None = Field(default=None, min_length=5)
    endereco: str | None = None
    municipio: str | None = None
    provincia: str | None = None
    horario_funcionamento: str | None = None
    acessivel: bool | None = None
    gratuita: bool | None = None
    capacidade_visitantes_dia: int | None = Field(default=None, gt=0)
    valor_entrada: Decimal | None = Field(default=None, ge=0)
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    observacoes: str | None = None
    ativa: bool | None = None

class AtracaoTuristicaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo: str
    nome: str
    tipo: TipoAtracao
    descricao: str
    endereco: str
    municipio: str
    provincia: str
    horario_funcionamento: str
    acessivel: bool
    gratuita: bool
    ativa: bool
    capacidade_visitantes_dia: int | None = None
    valor_entrada: Decimal | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    observacoes: str | None = None
