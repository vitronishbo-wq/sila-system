from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.resources.pecuaria.domain.enums import StatusPecuarista


class PecuaristaCreate(BaseModel):
    nome: str
    documento: str
    documento_tipo: str
    telefone: str | None = None
    email: str | None = None
    endereco: str | None = None
    citizen_id: UUID | None = None
    empresa_id: UUID | None = None
    observacoes: str | None = None


class PecuaristaAtivarInput(BaseModel):
    actor_id: UUID | None = None


class PecuaristaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    cadastro_pecuarista: str
    nome: str
    documento: str
    documento_tipo: str
    data_cadastro: date
    status: StatusPecuarista
    telefone: str | None = None
    email: str | None = None
    endereco: str | None = None
    citizen_id: UUID | None = None
    empresa_id: UUID | None = None
    observacoes: str | None = None


class PecuaristaFilter(BaseModel):
    status: StatusPecuarista | None = None
