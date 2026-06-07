from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class LicencaTurismoCreate(BaseModel):
    nome: str


class LicencaTurismoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    nome: str
