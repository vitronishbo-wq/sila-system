from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class EstatisticaTurismoCreate(BaseModel):
    nome: str


class EstatisticaTurismoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nome: str
