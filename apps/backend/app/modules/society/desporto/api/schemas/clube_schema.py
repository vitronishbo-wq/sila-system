from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.society.desporto.domain.enums import ModalidadeDesportiva, TipoClube

class ClubeCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    sigla: str = Field(..., min_length=2, max_length=10)
    tipo: TipoClube
    modalidade_principal: ModalidadeDesportiva
    municipio: str
    provincia: str
    data_fundacao: date | None = None
    codigo_obra_instalacao: str | None = None
    instituicao_educacional_id: UUID | None = None
    observacoes: str | None = None

class ClubeUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=3)
    sigla: str | None = Field(default=None, min_length=2, max_length=10)
    tipo: TipoClube | None = None
    modalidade_principal: ModalidadeDesportiva | None = None
    municipio: str | None = None
    provincia: str | None = None
    data_fundacao: date | None = None
    codigo_obra_instalacao: str | None = None
    instituicao_educacional_id: UUID | None = None
    ativo: bool | None = None
    observacoes: str | None = None

class ClubeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_clube: str
    nome: str
    sigla: str
    tipo: TipoClube
    modalidade_principal: ModalidadeDesportiva
    municipio: str
    provincia: str
    data_cadastro: date
    data_fundacao: date | None = None
    codigo_obra_instalacao: str | None = None
    instituicao_educacional_id: UUID | None = None
    ativo: bool
    observacoes: str | None = None