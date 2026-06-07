from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.resources.agricultura.domain.enums import StatusProdutor, TipoProdutor


class ProdutorCreate(BaseModel):
    nome: str
    documento: str
    documento_tipo: str
    tipo: TipoProdutor
    telefone: str | None = None
    email: str | None = None
    endereco: str | None = None
    citizen_id: UUID | None = None
    empresa_id: UUID | None = None
    observacoes: str | None = None


class ProdutorAtivarInput(BaseModel):
    actor_id: UUID | None = None


class ProdutorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    cadastro_produtor: str
    tipo: TipoProdutor
    status: StatusProdutor
    nome: str
    documento: str
    documento_tipo: str
    data_cadastro: date
    telefone: str | None = None
    email: str | None = None
    endereco: str | None = None
    citizen_id: UUID | None = None
    empresa_id: UUID | None = None
    familiar: bool
    observacoes: str | None = None


class ProdutorFilter(BaseModel):
    status: StatusProdutor | None = None
