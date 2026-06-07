from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import (
    StatusSLA,
    TipoServico,
)


class SLACreate(BaseModel):
    operadora_id: UUID
    nome: str = Field(..., min_length=3)
    servico: TipoServico
    disponibilidade_min_percentual: float = Field(..., ge=0, le=100)
    latencia_max_ms: float = Field(..., gt=0)
    jitter_max_ms: float = Field(..., ge=0)
    perda_pacotes_max_percentual: float = Field(..., ge=0, le=100)
    velocidade_download_min_mbps: float = Field(..., ge=0)
    velocidade_upload_min_mbps: float = Field(..., ge=0)
    data_inicio: date
    data_fim: date | None = None
    observacoes: str | None = None


class SLAStatusUpdate(BaseModel):
    status: StatusSLA


class SLAResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_sla: str
    operadora_id: UUID
    nome: str
    servico: TipoServico
    disponibilidade_min_percentual: float
    latencia_max_ms: float
    jitter_max_ms: float
    perda_pacotes_max_percentual: float
    velocidade_download_min_mbps: float
    velocidade_upload_min_mbps: float
    data_inicio: date
    data_fim: date | None = None
    status: StatusSLA
    ativo: bool
