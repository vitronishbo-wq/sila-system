from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.resources.pescas.industrial.domain.enums import (
    StatusInspecao,
    TipoSeloInspecao,
)


class InspecaoCreate(BaseModel):
    unidade_processamento_id: UUID
    data_agendada: date
    selo_inspecao: TipoSeloInspecao
    fiscal_id: UUID | None = None
    lote_producao_id: UUID | None = None
    observacoes: str | None = None


class InspecaoStatusUpdate(BaseModel):
    status: StatusInspecao
    pontuacao: int | None = Field(default=None, ge=0, le=100)
    aprovada: bool | None = None
    inconformidades: list[str] | None = None
    observacoes: str | None = None


class InspecaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_inspecao: str
    unidade_processamento_id: UUID
    data_agendada: date
    selo_inspecao: TipoSeloInspecao
    status: StatusInspecao
    fiscal_id: UUID | None = None
    lote_producao_id: UUID | None = None
    data_realizacao: date | None = None
    pontuacao: int | None = None
    inconformidades: list[str] | None = None
    observacoes: str | None = None
