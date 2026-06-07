from __future__ import annotations

from datetime import date
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.society.emprego.domain.enums import WorkflowStatus


class WorkflowCreate(BaseModel):
    citizen_id: UUID
    observacoes: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class WorkflowAction(BaseModel):
    actor_id: UUID
    observacoes: str | None = None


class WorkflowCancel(BaseModel):
    actor_id: UUID
    motivo: str = Field(..., min_length=3, max_length=500)


class WorkflowResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_processo: str
    citizen_id: UUID
    data_registro: date
    service_type: str
    status: WorkflowStatus
    observacoes: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
