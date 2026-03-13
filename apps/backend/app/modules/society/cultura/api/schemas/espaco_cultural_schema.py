from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.modules.society.cultura.domain.enums import TipoEspacoCultural

class EspacoCulturalCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    tipo: TipoEspacoCultural
    municipio: str = Field(..., min_length=2)
    provincia: str = Field(..., min_length=2)
    endereco: str = Field(..., min_length=3)
    capacidade: int = Field(..., gt=0)
    area_m2: float = Field(..., gt=0)
    administracao: str = Field(..., min_length=3)
    responsavel_cpf: str = Field(..., min_length=5)
    orgao_gestor: str | None = None
    ano_inauguracao: int | None = None
    acessibilidade: bool = False
    observacoes: str | None = None

class EspacoCulturalUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=3)
    tipo: TipoEspacoCultural | None = None
    municipio: str | None = Field(default=None, min_length=2)
    provincia: str | None = Field(default=None, min_length=2)
    endereco: str | None = Field(default=None, min_length=3)
    capacidade: int | None = Field(default=None, gt=0)
    area_m2: float | None = Field(default=None, gt=0)
    administracao: str | None = None
    responsavel_cpf: str | None = None
    orgao_gestor: str | None = None
    ano_inauguracao: int | None = None
    acessibilidade: bool | None = None
    ativo: bool | None = None
    observacoes: str | None = None

class EspacoCulturalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_espaco: str
    nome: str
    tipo: TipoEspacoCultural
    municipio: str
    provincia: str
    endereco: str
    capacidade: int
    area_m2: float
    administracao: str
    responsavel_cpf: str
    data_registro: date
    orgao_gestor: str | None = None
    ano_inauguracao: int | None = None
    acessibilidade: bool
    visitas_anuais: int
    ativo: bool
    observacoes: str | None = None