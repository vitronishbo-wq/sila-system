from __future__ import annotations
from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.resources.pecuaria.domain.enums import StatusPecuarista

class PecuaristaCreate(BaseModel):
    nome: str
    documento: str
    documento_tipo: str
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    citizen_id: Optional[UUID] = None
    empresa_id: Optional[UUID] = None
    observacoes: Optional[str] = None

class PecuaristaAtivarInput(BaseModel):
    actor_id: Optional[UUID] = None

class PecuaristaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    cadastro_pecuarista: str
    nome: str
    documento: str
    documento_tipo: str
    data_cadastro: date
    status: StatusPecuarista
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    citizen_id: Optional[UUID] = None
    empresa_id: Optional[UUID] = None
    observacoes: Optional[str] = None

class PecuaristaFilter(BaseModel):
    status: Optional[StatusPecuarista] = None