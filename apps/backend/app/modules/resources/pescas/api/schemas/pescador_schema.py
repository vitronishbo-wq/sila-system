from __future__ import annotations
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.modules.resources.pescas.domain.enums import TipoPescador

class PescadorCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    tipo: TipoPescador
    citizen_id: UUID
    numero_registro: Optional[str] = None

class PescadorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    nome: str
    numero_registro: str
    tipo: TipoPescador
    citizen_id: UUID
    ativo: bool

class PescadorFilter(BaseModel):
    tipo: Optional[TipoPescador] = None