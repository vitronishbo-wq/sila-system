from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.infrastructure.domain.enums import StatusProjeto, TipoProjeto


class ProjetoCreate(BaseModel):
    nome: str
    tipo: TipoProjeto
    orgao_responsavel_id: UUID
    responsavel_tecnico_id: UUID
    valor_estimado: Decimal
    data_inicio_prevista: date
    data_fim_prevista: date
    codigo_projeto: str | None = None
    obra_id: UUID | None = None
    descricao: str | None = None


class ProjetoInicioInput(BaseModel):
    data_inicio: date


class ProjetoConclusaoInput(BaseModel):
    data_fim: date


class ProjetoMotivoInput(BaseModel):
    motivo: str


class ProjetoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_projeto: str
    nome: str
    tipo: TipoProjeto
    status: StatusProjeto
    orgao_responsavel_id: UUID
    responsavel_tecnico_id: UUID
    valor_estimado: Decimal
    data_inicio_prevista: date
    data_fim_prevista: date
    data_cadastro: date
    obra_id: UUID | None = None
    descricao: str | None = None
    data_inicio_real: date | None = None
    data_fim_real: date | None = None
    versao: int
    data_atualizacao: date | None = None
    observacoes: str | None = None
