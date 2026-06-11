from __future__ import annotations

from datetime import date
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

# Importa o Enum canónico da sua fonte única de verdade no domínio
from apps.backend.app.modules.educacao.domain.enums import CanonicalStatus


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
    
    # O campo de status agora usa o Enum canónico, garantindo consistência
    # em todos os fluxos de trabalho que herdam deste schema.
    status: CanonicalStatus
    
    observacoes: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
