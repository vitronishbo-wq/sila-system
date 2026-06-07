from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import (
    StatusOperacaoUrbana,
    TipoOperacaoUrbana,
)


class OperacaoUrbanaCreate(BaseModel):
    nome: str
    tipo: TipoOperacaoUrbana
    plano_diretor_id: UUID
    orgao_responsavel_id: UUID
    provincia: str
    municipio: str | None = None
    area_intervencao: Decimal | None = None
    investimento_previsto: Decimal | None = None
    data_inicio_prevista: date | None = None
    data_fim_prevista: date | None = None
    codigo_operacao: str | None = None


class OperacaoUrbanaInicioInput(BaseModel):
    data_inicio_real: date


class OperacaoUrbanaExecucaoInput(BaseModel):
    percentual_execucao: Decimal
    investimento_executado: Decimal | None = None


class OperacaoUrbanaConclusaoInput(BaseModel):
    data_fim_real: date


class OperacaoUrbanaMotivoInput(BaseModel):
    motivo: str


class OperacaoUrbanaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_operacao: str
    nome: str
    tipo: TipoOperacaoUrbana
    status: StatusOperacaoUrbana
    plano_diretor_id: UUID
    orgao_responsavel_id: UUID
    provincia: str
    municipio: str | None = None
    area_intervencao: Decimal | None = None
    investimento_previsto: Decimal | None = None
    investimento_executado: Decimal | None = None
    data_inicio_prevista: date | None = None
    data_fim_prevista: date | None = None
    data_inicio_real: date | None = None
    data_fim_real: date | None = None
    percentual_execucao: Decimal
    data_cadastro: date
    data_atualizacao: date | None = None
    observacoes: str | None = None
