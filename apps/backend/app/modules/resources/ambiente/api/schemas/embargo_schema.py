from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.resources.ambiente.domain.enums import StatusEmbargo

class EmbargoCreate(BaseModel):
    numero_auto_infracao: str
    motivo: str

class EmbargoSuspensaoInput(BaseModel):
    motivo: str

class EmbargoLevantamentoInput(BaseModel):
    observacoes: str | None = None

class EmbargoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_embargo: str
    numero_auto_infracao: str
    motivo: str
    status: StatusEmbargo
    data_aplicacao: date
    data_levantamento: date | None = None
    observacoes: str | None = None