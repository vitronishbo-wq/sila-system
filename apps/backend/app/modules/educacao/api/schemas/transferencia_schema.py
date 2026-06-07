from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from apps.backend.app.modules.educacao.api.schemas.workflow_schema import WorkflowResponse


class TransferenciaCreate(BaseModel):
    matricula_id: UUID
    escola_destino_id: UUID
    turma_destino_id: UUID
    motivo: str = Field(..., min_length=3, max_length=500)
    observacoes: str | None = None


class TransferenciaAprovar(BaseModel):
    resumo: str | None = Field(default=None, max_length=500)


class TransferenciaRejeitar(BaseModel):
    motivo: str = Field(..., min_length=3, max_length=500)


class TransferenciaResponse(WorkflowResponse):
    pass


class TransferTransactionCreate(BaseModel):
    student_id: UUID
    current_enrollment_id: UUID
    target_institution_id: UUID
    target_grade: str = Field(..., min_length=1, max_length=64)
    target_shift: str = Field(..., min_length=1, max_length=64)
    academic_year: str = Field(..., min_length=4, max_length=16)
    reason: str = Field(..., min_length=3, max_length=500)


class TransferTransactionResponse(BaseModel):
    status: str
    transfer_id: str
    old_enrollment_id: str
    new_enrollment_id: str
    academic_year: str
    steps_completed: list[str]
    audit_trail: list[dict[str, Any]]
    audit_event: dict[str, Any]
    domain_event: dict[str, Any]
    receipt: dict[str, Any]
