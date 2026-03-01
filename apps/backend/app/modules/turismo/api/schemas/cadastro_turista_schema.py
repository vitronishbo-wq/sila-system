from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CadastroTuristaCreate(BaseModel):
    nome: str


class CadastroTuristaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nome: str
