from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.modules.turismo.domain.enums import ClassificacaoHoteleira, TipoMeioHospedagem


class HotelCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    tipo: TipoMeioHospedagem
    classificacao: ClassificacaoHoteleira
    cnpj: str = Field(..., pattern=r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$")
    endereco: str
    numero: str
    bairro: str
    municipio: str
    provincia: str
    cep: str
    telefone: str
    email: str = Field(..., pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    quartos: int = Field(..., gt=0)
    capacidade_maxima: int = Field(..., gt=0)
    proprietario_id: UUID


class HotelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    cadastur: str
    nome: str
    tipo: TipoMeioHospedagem
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
    categoria_estrelas: int
    proprietario_id: UUID
    data_abertura: date
