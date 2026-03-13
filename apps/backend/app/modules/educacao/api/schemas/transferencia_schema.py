from __future__ import annotations
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from apps.backend.app.modules.educacao.api.schemas.workflow_schema import WorkflowResponse

class TransferenciaCreate(BaseModel):
    matricula_id: UUID
    escola_destino_id: UUID
    turma_destino_id: UUID
    motivo: str = Field(..., min_length=3, max_length=500)
    observacoes: Optional[str] = None

class TransferenciaAprovar(BaseModel):
    resumo: Optional[str] = Field(default=None, max_length=500)

class TransferenciaRejeitar(BaseModel):
    motivo: str = Field(..., min_length=3, max_length=500)

class TransferenciaResponse(WorkflowResponse):
    pass