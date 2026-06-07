from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.resources.pecuaria.domain.enums import Sexo, StatusAnimal, TipoAnimal


class AnimalCreate(BaseModel):
    brinco: str | None = Field(default=None, min_length=3, max_length=20)
    tipo: TipoAnimal
    raca_id: UUID
    sexo: Sexo
    data_nascimento: date
    proprietario_id: UUID
    propriedade_id: UUID
    rebanho_id: UUID | None = None


class AnimalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    brinco: str
    nome: str | None = None
    tipo: TipoAnimal
    raca_id: UUID
    sexo: Sexo
    data_nascimento: date
    peso_atual: Decimal | None = None
    status: StatusAnimal
    proprietario_id: UUID
    propriedade_id: UUID
    rebanho_id: UUID | None = None


class AnimalFilter(BaseModel):
    tipo: TipoAnimal | None = None
    status: StatusAnimal | None = None
    propriedade_id: UUID | None = None
