from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OcupacaoHoteleiraCreate(BaseModel):
    nome: str


class OcupacaoHoteleiraResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nome: str
