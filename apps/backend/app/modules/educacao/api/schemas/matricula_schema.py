from __future__ import annotations

from datetime import date
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.educacao.domain.models import StatusMatricula


class MatriculaCreate(BaseModel):
    citizen_id: UUID = Field(..., description="ID do cidadao no nucleo identity")
    escola_id: UUID
    turma_id: UUID
    ano_letivo_id: UUID
    observacoes: str | None = None


class MatriculaAtivar(BaseModel):
    confirmacao_documental: Literal[True]


class MatriculaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_processo: str
    citizen_id: UUID
    escola_id: UUID
    turma_id: UUID
    ano_letivo_id: UUID
    data_matricula: date
    status: StatusMatricula
    observacoes: str | None = None


class MatriculaListFilter(BaseModel):
    ano_letivo_id: UUID | None = None
    escola_id: UUID | None = None
    status: StatusMatricula | None = None
