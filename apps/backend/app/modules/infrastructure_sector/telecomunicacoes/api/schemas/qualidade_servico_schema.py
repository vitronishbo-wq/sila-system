from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import (
    StatusQualidadeServico,
    TipoServico,
)


class QualidadeServicoCreate(BaseModel):
    operadora_id: UUID
    servico: TipoServico
    data_medicao: date
    disponibilidade_percentual: float = Field(..., ge=0, le=100)
    latencia_ms: float = Field(..., ge=0)
    jitter_ms: float = Field(..., ge=0)
    perda_pacotes_percentual: float = Field(..., ge=0, le=100)
    velocidade_download_mbps: float = Field(..., ge=0)
    velocidade_upload_mbps: float = Field(..., ge=0)
    assinante_id: UUID | None = None
    sla_id: UUID | None = None
    observacoes: str | None = None


class QualidadeServicoStatusUpdate(BaseModel):
    status: StatusQualidadeServico


class QualidadeServicoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_medicao: str
    operadora_id: UUID
    servico: TipoServico
    data_medicao: date
    disponibilidade_percentual: float
    latencia_ms: float
    jitter_ms: float
    perda_pacotes_percentual: float
    velocidade_download_mbps: float
    velocidade_upload_mbps: float
    status: StatusQualidadeServico
    assinante_id: UUID | None = None
    sla_id: UUID | None = None
    ativo: bool
