from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.tourism.domain.enums import ClassificacaoHoteleira


class PousadaCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    classificacao: ClassificacaoHoteleira
    cnpj: str = Field(..., pattern="^\\d{2}\\.\\d{3}\\.\\d{3}/\\d{4}-\\d{2}$")
    endereco: str
    numero: str
    bairro: str
    municipio: str
    provincia: str
    cep: str
    telefone: str
    email: str = Field(..., pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$")
    quartos: int = Field(..., gt=0)
    capacidade_maxima: int = Field(..., gt=0)
    proprietario_id: UUID


class PousadaUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=3)
    classificacao: ClassificacaoHoteleira | None = None
    endereco: str | None = None
    numero: str | None = None
    bairro: str | None = None
    municipio: str | None = None
    provincia: str | None = None
    cep: str | None = None
    telefone: str | None = None
    email: str | None = Field(
        default=None, pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    )
    site: str | None = None
    observacoes: str | None = None
    ativa: bool | None = None


class PousadaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    cadastur: str
    nome: str
    classificacao: ClassificacaoHoteleira
    cnpj: str
    endereco: str
    numero: str
    bairro: str
    municipio: str
    provincia: str
    cep: str
    telefone: str
    email: str
    quartos: int
    capacidade_maxima: int
    proprietario_id: UUID
    data_abertura: date
    ativa: bool
    site: str | None = None
    observacoes: str | None = None
