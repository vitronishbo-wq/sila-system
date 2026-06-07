from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CadasturCreate(BaseModel):
    nome: str


class CadasturResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    nome: str
