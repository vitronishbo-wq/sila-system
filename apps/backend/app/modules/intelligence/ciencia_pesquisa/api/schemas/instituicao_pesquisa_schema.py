from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.intelligence.ciencia_pesquisa.domain.enums import NaturezaJuridicaInstituicao, StatusCredenciamentoInstituicao, TipoInstituicaoPesquisa

class InstituicaoPesquisaCreate(BaseModel):
    sigla: str = Field(..., min_length=2)
    nome: str = Field(..., min_length=3)
    nif: str = Field(..., min_length=3)
    tipo: TipoInstituicaoPesquisa
    natureza_juridica: NaturezaJuridicaInstituicao
    pais: str = Field(..., min_length=2)
    provincia: str = Field(..., min_length=2)
    municipio: str = Field(..., min_length=2)
    endereco: str = Field(..., min_length=3)
    email_institucional: str = Field(..., min_length=5)
    telefone: str | None = None
    website: str | None = None

class InstituicaoPesquisaCredenciarInput(BaseModel):
    data_credenciamento: date | None = None
    data_validade_credenciamento: date | None = None

class InstituicaoPesquisaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    sigla: str
    nome: str
    nif: str
    tipo: TipoInstituicaoPesquisa
    natureza_juridica: NaturezaJuridicaInstituicao
    pais: str
    provincia: str
    municipio: str
    endereco: str
    email_institucional: str
    telefone: str | None = None
    website: str | None = None
    status_credenciamento: StatusCredenciamentoInstituicao
    data_credenciamento: date | None = None
    data_validade_credenciamento: date | None = None
    comite_etica_ativo: bool
    nucleo_inovacao_ativo: bool
    ativa: bool