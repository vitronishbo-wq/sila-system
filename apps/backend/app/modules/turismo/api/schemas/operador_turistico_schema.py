from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OperadorTuristicoCreate(BaseModel):
    nome: str


class OperadorTuristicoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nome: str
