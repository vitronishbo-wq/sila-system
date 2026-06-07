from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class VacinaCreate(BaseModel):
    animal_id: UUID
    nome: str
    data_aplicacao: date
    proxima_dose: date | None = None


class VacinaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    animal_id: UUID
    nome: str
    data_aplicacao: date
    proxima_dose: date | None = None
