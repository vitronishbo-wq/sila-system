from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.modules.intelligence.ciencia_pesquisa.domain.enums import AreaConhecimento, NivelFormacao, StatusVinculoPesquisador, TipoVinculoPesquisador

class PesquisadorCreate(BaseModel):
    nome_completo: str = Field(..., min_length=3)
    documento_identificacao: str = Field(..., min_length=3)
    email_institucional: str = Field(..., min_length=5)
    instituicao_id: UUID | None = None
    unidade_pesquisa_id: UUID | None = None
    area_conhecimento: AreaConhecimento = AreaConhecimento.MULTIDISCIPLINAR
    nivel_formacao: NivelFormacao = NivelFormacao.GRADUADO
    tipo_vinculo: TipoVinculoPesquisador = TipoVinculoPesquisador.EFETIVO
    data_inicio_vinculo: date | None = None
    telefone: str | None = None
    orcid: str | None = None
    lattes_url: str | None = None
    researcher_id: str | None = None
    scopus_id: str | None = None

class PesquisadorVincularInstituicaoInput(BaseModel):
    instituicao_id: UUID
    unidade_pesquisa_id: UUID | None = None

class PesquisadorEncerrarVinculoInput(BaseModel):
    data_fim_vinculo: date | None = None

class PesquisadorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    nome_completo: str
    documento_identificacao: str
    email_institucional: str
    instituicao_id: UUID | None = None
    unidade_pesquisa_id: UUID | None = None
    area_conhecimento: AreaConhecimento
    nivel_formacao: NivelFormacao
    tipo_vinculo: TipoVinculoPesquisador
    status_vinculo: StatusVinculoPesquisador
    data_inicio_vinculo: date
    data_fim_vinculo: date | None = None
    telefone: str | None = None
    orcid: str | None = None
    lattes_url: str | None = None
    researcher_id: str | None = None
    scopus_id: str | None = None
    ativo: bool