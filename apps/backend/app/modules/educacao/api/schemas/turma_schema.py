from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.educacao.domain.turma import Turno


class TurmaCreate(BaseModel):
    escola_id: UUID
    ano_letivo_id: UUID
    codigo: str = Field(..., max_length=32)
    classe: str = Field(..., max_length=32)
    turno: Turno
    capacidade: int = Field(default=40, ge=1)


class TurmaUpdate(BaseModel):
    """Schema para atualização parcial de uma turma."""
    codigo: str | None = Field(default=None, max_length=32)
    classe: str | None = Field(default=None, max_length=32)
    turno: Turno | None = None
    capacidade: int | None = Field(default=None, ge=1)
    ativa: bool | None = None


class TurmaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    escola_id: UUID
    ano_letivo_id: UUID
    codigo: str
    classe: str
    turno: str
    capacidade: int
    ativa: bool
    territory_id: UUID | None = None
    created_by: UUID | None = None
    managed_by: UUID | None = None
