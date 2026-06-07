from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.society.desporto.domain.enums import (
    ModalidadeDesportiva,
    StatusCompeticao,
    TipoCompeticao,
)


class CompeticaoCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    tipo: TipoCompeticao
    modalidade: ModalidadeDesportiva
    data_inicio: date
    data_fim: date
    municipio: str
    provincia: str
    organizador_id: UUID
    codigo_obra_instalacao: str | None = None
    atracao_turistica_id: UUID | None = None
    instituicao_educacional_id: UUID | None = None
    premiacao_total: Decimal | None = Field(default=None, ge=0)
    observacoes: str | None = None


class CompeticaoUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=3)
    tipo: TipoCompeticao | None = None
    modalidade: ModalidadeDesportiva | None = None
    data_inicio: date | None = None
    data_fim: date | None = None
    municipio: str | None = None
    provincia: str | None = None
    codigo_obra_instalacao: str | None = None
    atracao_turistica_id: UUID | None = None
    instituicao_educacional_id: UUID | None = None
    premiacao_total: Decimal | None = Field(default=None, ge=0)
    inscricoes_abertas: bool | None = None
    status: StatusCompeticao | None = None
    ativo: bool | None = None
    observacoes: str | None = None


class CompeticaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_competicao: str
    nome: str
    tipo: TipoCompeticao
    modalidade: ModalidadeDesportiva
    data_inicio: date
    data_fim: date
    municipio: str
    provincia: str
    organizador_id: UUID
    data_cadastro: date
    status: StatusCompeticao
    codigo_obra_instalacao: str | None = None
    atracao_turistica_id: UUID | None = None
    instituicao_educacional_id: UUID | None = None
    premiacao_total: Decimal | None = None
    inscricoes_abertas: bool
    ativo: bool
    observacoes: str | None = None
