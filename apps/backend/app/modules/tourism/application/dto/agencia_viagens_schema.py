from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class AgenciaViagensCreate(BaseModel):
    nome_fantasia: str = Field(..., min_length=3)
    razao_social: str = Field(..., min_length=3)
    cnpj: str = Field(..., pattern='^\\d{2}\\.\\d{3}\\.\\d{3}/\\d{4}-\\d{2}$')
    email: str = Field(..., pattern='^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$')
    telefone: str
    endereco: str
    numero: str
    bairro: str
    municipio: str
    provincia: str
    cep: str
    proprietario_id: UUID
    especialidades: list[str] | None = None
    site: str | None = None
    observacoes: str | None = None

class AgenciaViagensUpdate(BaseModel):
    nome_fantasia: str | None = Field(default=None, min_length=3)
    razao_social: str | None = Field(default=None, min_length=3)
    email: str | None = Field(default=None, pattern='^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$')
    telefone: str | None = None
    endereco: str | None = None
    numero: str | None = None
    bairro: str | None = None
    municipio: str | None = None
    provincia: str | None = None
    cep: str | None = None
    especialidades: list[str] | None = None
    site: str | None = None
    observacoes: str | None = None
    ativa: bool | None = None

class AgenciaViagensResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    registro: str
    nome_fantasia: str
    razao_social: str
    cnpj: str
    email: str
    telefone: str
    endereco: str
    numero: str
    bairro: str
    municipio: str
    provincia: str
    cep: str
    proprietario_id: UUID
    data_registro: date
    ativa: bool
    especialidades: list[str] | None = None
    site: str | None = None
    observacoes: str | None = None