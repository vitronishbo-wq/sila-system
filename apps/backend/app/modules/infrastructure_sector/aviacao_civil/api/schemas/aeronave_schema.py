from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.domain.enums import CategoriaAeronave, StatusAeronavegabilidade, TipoAeronave

class AeronaveCreate(BaseModel):
    matricula: str = Field(min_length=3, max_length=10)
    tipo: TipoAeronave
    categoria: CategoriaAeronave
    fabricante: str = Field(min_length=2, max_length=100)
    modelo: str = Field(min_length=1, max_length=100)
    numero_serie: str = Field(min_length=3, max_length=60)
    ano_fabricacao: int = Field(ge=1903, le=2100)
    proprietario_cpf_cnpj: str = Field(min_length=5, max_length=20)
    capacidade_passageiros: int = Field(default=0, ge=0)
    autonomia_km: float = Field(default=0.0, ge=0)
    peso_maximo_decolagem_kg: float = Field(default=0.0, ge=0)

class AeronaveResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    matricula: str
    tipo: TipoAeronave
    categoria: CategoriaAeronave
    fabricante: str
    modelo: str
    numero_serie: str
    ano_fabricacao: int
    proprietario_cpf_cnpj: str
    capacidade_passageiros: int
    autonomia_km: float
    peso_maximo_decolagem_kg: float
    status_aeronavegabilidade: StatusAeronavegabilidade
    horas_voadas_total: float
    ciclos_total: int
    data_registro: datetime