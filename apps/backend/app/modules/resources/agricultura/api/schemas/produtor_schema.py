from __future__ import annotations
from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusProdutor, TipoProdutor

class ProdutorCreate(BaseModel):
    nome: str
    documento: str
    documento_tipo: str
    tipo: TipoProdutor
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    citizen_id: Optional[UUID] = None
    empresa_id: Optional[UUID] = None
    observacoes: Optional[str] = None

class ProdutorAtivarInput(BaseModel):
    actor_id: Optional[UUID] = None

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
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    citizen_id: Optional[UUID] = None
    empresa_id: Optional[UUID] = None
    familiar: bool
    observacoes: Optional[str] = None

class ProdutorFilter(BaseModel):
    status: Optional[StatusProdutor] = None