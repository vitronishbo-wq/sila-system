from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.civil_protection.domain.enums import (
    CargoBombeiro,
    StatusAgenteProtecao,
)


class BombeiroCreate(BaseModel):
    corporacao_id: UUID
    nome: str = Field(..., min_length=3)
    data_nascimento: date
    cpf: str = Field(..., min_length=14, max_length=14)
    rg: str
    cargo: CargoBombeiro | None = None
    telefone: str | None = None
    email: str | None = None
    endereco: str | None = None
    observacoes: str | None = None
    citizen_id: UUID | None = None


class BombeiroStatusUpdate(BaseModel):
    status: StatusAgenteProtecao
    motivo: str | None = None


class BombeiroResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    matricula: str
    corporacao_id: UUID
    nome: str
    data_nascimento: date
    cpf: str
    cargo: CargoBombeiro | None
    status: StatusAgenteProtecao
    ativo: bool
