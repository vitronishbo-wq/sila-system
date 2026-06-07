from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import (
    StatusLoteamento,
    TipoLoteamento,
)


class LoteamentoCreate(BaseModel):
    nome: str
    tipo: TipoLoteamento
    parcelamento_id: UUID
    plano_diretor_id: UUID
    zoneamento_id: UUID
    provincia: str
    area_total: Decimal
    quantidade_lotes_prevista: int
    municipio: str | None = None
    area_lotes: Decimal | None = None
    area_verde: Decimal | None = None
    area_institucional: Decimal | None = None
    data_inicio_prevista: date | None = None
    data_fim_prevista: date | None = None
    codigo_loteamento: str | None = None


class LoteamentoInicioInput(BaseModel):
    data_inicio_real: date


class LoteamentoImplantacaoInput(BaseModel):
    quantidade_lotes_implantada: int


class LoteamentoConclusaoInput(BaseModel):
    data_fim_real: date


class LoteamentoMotivoInput(BaseModel):
    motivo: str


class LoteamentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_loteamento: str
    nome: str
    tipo: TipoLoteamento
    status: StatusLoteamento
    parcelamento_id: UUID
    plano_diretor_id: UUID
    zoneamento_id: UUID
    provincia: str
    area_total: Decimal
    quantidade_lotes_prevista: int
    municipio: str | None = None
    quantidade_lotes_implantada: int
    area_lotes: Decimal | None = None
    area_verde: Decimal | None = None
    area_institucional: Decimal | None = None
    data_inicio_prevista: date | None = None
    data_fim_prevista: date | None = None
    data_inicio_real: date | None = None
    data_fim_real: date | None = None
    data_cadastro: date
    data_atualizacao: date | None = None
    observacoes: str | None = None
