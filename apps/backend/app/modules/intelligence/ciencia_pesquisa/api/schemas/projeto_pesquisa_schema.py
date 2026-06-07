from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.intelligence.ciencia_pesquisa.domain.enums import (
    AreaConhecimento,
    StatusProjetoPesquisa,
)


class ProjetoPesquisaCreate(BaseModel):
    titulo: str = Field(..., min_length=5)
    resumo: str = Field(..., min_length=10)
    instituicao_id: UUID
    coordenador_id: UUID
    equipe_pesquisadores_ids: list[UUID] = Field(default_factory=list)
    area_conhecimento: AreaConhecimento = AreaConhecimento.MULTIDISCIPLINAR
    data_inicio: date | None = None
    data_fim_prevista: date | None = None
    palavras_chave: list[str] = Field(default_factory=list)
    orcamento_previsto: float | None = None
    codigo_projeto: str | None = None


class ProjetoPesquisaVincularPesquisadoresInput(BaseModel):
    pesquisador_ids: list[UUID] = Field(..., min_length=1)


class ProjetoPesquisaEncerrarInput(BaseModel):
    data_fim_real: date | None = None


class ProjetoPesquisaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_projeto: str
    titulo: str
    resumo: str
    instituicao_id: UUID
    coordenador_id: UUID
    equipe_pesquisadores_ids: list[UUID]
    area_conhecimento: AreaConhecimento
    data_inicio: date
    data_fim_prevista: date | None = None
    data_fim_real: date | None = None
    status: StatusProjetoPesquisa
    palavras_chave: list[str] | None = None
    orcamento_previsto: float | None = None
    ativo: bool
