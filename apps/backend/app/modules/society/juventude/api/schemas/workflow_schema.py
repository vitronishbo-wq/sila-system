from __future__ import annotations

from datetime import date
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.society.juventude.domain.enums import StatusFluxo


class WorkflowCreate(BaseModel):
    citizen_id: UUID
    instituicao_id: UUID
    observacoes: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class WorkflowConcluir(BaseModel):
    resumo: str | None = Field(default=None, max_length=500)


class WorkflowCancelar(BaseModel):
    motivo: str = Field(..., min_length=3, max_length=500)


class WorkflowResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_processo: str
    service_type: str
    citizen_id: UUID
    instituicao_id: UUID
    data_registo: date
    status: StatusFluxo
    observacoes: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
