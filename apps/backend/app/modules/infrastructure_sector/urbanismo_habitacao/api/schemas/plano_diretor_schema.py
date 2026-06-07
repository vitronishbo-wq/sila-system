from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import (
    StatusPlanoDiretor,
    TipoPlanoDiretor,
)


class PlanoDiretorCreate(BaseModel):
    nome: str
    tipo: TipoPlanoDiretor
    provincia: str
    ano_elaboracao: int
    orgao_responsavel_id: UUID
    municipio: str | None = None
    codigo_plano: str | None = None


class PlanoDiretorAudienciaInput(BaseModel):
    participantes: int


class PlanoDiretorAprovacaoCamaraInput(BaseModel):
    lei_aprovacao: str
    ano_aprovacao: int


class PlanoDiretorSancaoInput(BaseModel):
    data_publicacao: date


class PlanoDiretorValidadeInput(BaseModel):
    data_inicio: date
    data_fim: date


class PlanoDiretorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_plano: str
    nome: str
    tipo: TipoPlanoDiretor
    status: StatusPlanoDiretor
    provincia: str
    ano_elaboracao: int
    orgao_responsavel_id: UUID
    municipio: str | None = None
    ano_aprovacao: int | None = None
    ano_publicacao: int | None = None
    periodo_validade_inicio: date | None = None
    periodo_validade_fim: date | None = None
    lei_aprovacao: str | None = None
    participantes_consulta: int | None = None
    audiencias_publicas: int | None = None
    documento_url: str | None = None
    mapa_url: str | None = None
    area_total_urbana: Decimal | None = None
    area_total_rural: Decimal | None = None
    populacao_estimada: int | None = None
    densidade_media: Decimal | None = None
    macrozoneamento: list[dict] | None = None
    diretrizes_gerais: str | None = None
    objetivos_estrategicos: str | None = None
    observacoes: str | None = None
    data_publicacao: date | None = None
