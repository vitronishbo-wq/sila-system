from __future__ import annotations
from datetime import date
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.modules.resources.pecuaria.domain.enums import Sexo, StatusAnimal, TipoAnimal

class AnimalCreate(BaseModel):
    brinco: Optional[str] = Field(default=None, min_length=3, max_length=20)
    tipo: TipoAnimal
    raca_id: UUID
    sexo: Sexo
    data_nascimento: date
    proprietario_id: UUID
    propriedade_id: UUID
    rebanho_id: Optional[UUID] = None

class AnimalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    brinco: str
    nome: Optional[str] = None
    tipo: TipoAnimal
    raca_id: UUID
    sexo: Sexo
    data_nascimento: date
    peso_atual: Optional[Decimal] = None
    status: StatusAnimal
    proprietario_id: UUID
    propriedade_id: UUID
    rebanho_id: Optional[UUID] = None

class AnimalFilter(BaseModel):
    tipo: Optional[TipoAnimal] = None
    status: Optional[StatusAnimal] = None
    propriedade_id: Optional[UUID] = None