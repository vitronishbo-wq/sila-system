from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.modules.society.juventude.domain.enums import Escolaridade, FaixaEtaria, SituacaoOcupacional, TipoVulnerabilidade

class JovemCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    data_nascimento: date
    genero: str
    naturalidade: str
    nacionalidade: str = 'Angolana'
    escolaridade: Escolaridade
    situacao_ocupacional: SituacaoOcupacional
    endereco: str
    municipio: str
    provincia: str
    telefone: str | None = None
    email: str | None = None
    citizen_id: UUID | None = None
    observacoes: str | None = None

class JovemUpdate(BaseModel):
    escolaridade: Escolaridade | None = None
    situacao_ocupacional: SituacaoOcupacional | None = None
    telefone: str | None = None
    email: str | None = None
    endereco: str | None = None
    municipio: str | None = None
    provincia: str | None = None
    observacoes: str | None = None
    ativo: bool | None = None

class VulnerabilidadeAdd(BaseModel):
    vulnerabilidade: TipoVulnerabilidade

class JovemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_registro: str
    nome: str
    data_nascimento: date
    faixa_etaria: FaixaEtaria
    genero: str
    naturalidade: str
    nacionalidade: str
    escolaridade: Escolaridade
    situacao_ocupacional: SituacaoOcupacional
    endereco: str
    municipio: str
    provincia: str
    telefone: str | None = None
    email: str | None = None
    citizen_id: UUID | None = None
    vulnerabilidades: list[TipoVulnerabilidade] | None = None
    auxilios: list[UUID] | None = None
    data_cadastro: date
    observacoes: str | None = None
    ativo: bool