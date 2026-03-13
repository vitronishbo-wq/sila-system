from __future__ import annotations
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class ArmadorCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    nif: str = Field(..., min_length=5)

class ArmadorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    nome: str
    nif: str
    ativo: bool

class ArmadorFilter(BaseModel):
    ativo: Optional[bool] = None