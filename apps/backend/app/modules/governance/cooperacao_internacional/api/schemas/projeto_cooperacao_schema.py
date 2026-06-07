from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.governance.cooperacao_internacional.domain.enums import (
    ModalidadeCooperacao,
    StatusProjeto,
    TipoProjeto,
)


class ProjetoCooperacaoCreate(BaseModel):
    titulo: str = Field(min_length=5, max_length=300)
    tipo: TipoProjeto
    modalidade: ModalidadeCooperacao
    acordo_base_id: UUID | None = None
    orgao_responsavel_id: UUID
    orgao_parceiro_id: UUID
    pais_parceiro_id: UUID
    data_inicio: date
    data_fim: date
    objetivo_geral: str = Field(min_length=10, max_length=4000)
    objetivos_especificos: list[str] = Field(default_factory=list)
    orcamento_total: float = Field(gt=0)
    fonte_recursos: str = Field(min_length=2, max_length=200)


class ProjetoCooperacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_projeto: str
    titulo: str
    tipo: TipoProjeto
    modalidade: ModalidadeCooperacao
    acordo_base_id: UUID | None
    orgao_responsavel_id: UUID
    orgao_parceiro_id: UUID
    pais_parceiro_id: UUID
    data_inicio: date
    data_fim: date
    objetivo_geral: str
    objetivos_especificos: list[str]
    orcamento_total: float
    fonte_recursos: str
    status: StatusProjeto
    atividades: list[dict]
