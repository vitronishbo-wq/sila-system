from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import (
    StatusIndicadorQualidade,
)


class IndicadorQualidadeGerar(BaseModel):
    operadora_id: UUID
    referencia_ano: int = Field(..., ge=2000)
    referencia_mes: int = Field(..., ge=1, le=12)
    observacoes: str | None = None


class IndicadorQualidadeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_indicador: str
    operadora_id: UUID
    referencia_ano: int
    referencia_mes: int
    total_medicoes: int
    disponibilidade_media_percentual: float
    latencia_media_ms: float
    jitter_medio_ms: float
    perda_pacotes_media_percentual: float
    conformidade_percentual: float
    data_calculo: date
    status: StatusIndicadorQualidade
    ativo: bool
