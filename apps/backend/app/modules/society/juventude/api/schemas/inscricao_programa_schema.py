from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.society.juventude.domain.enums import StatusInscricao


class InscricaoProgramaCreate(BaseModel):
    programa_id: UUID
    jovem_id: UUID
    prioridade: int = Field(default=0, ge=0)
    observacoes: str | None = None


class InscricaoProgramaCancelar(BaseModel):
    motivo: str | None = None


class InscricaoProgramaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_inscricao: str
    programa_id: UUID
    jovem_id: UUID
    data_inscricao: date
    status: StatusInscricao
    prioridade: int
    data_cadastro: date
    observacoes: str | None = None
    ativo: bool
