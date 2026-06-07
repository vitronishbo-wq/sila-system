from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProducaoLeiteCreate(BaseModel):
    propriedade_id: UUID
    litros: float
    data_producao: date


class ProducaoCarneCreate(BaseModel):
    propriedade_id: UUID
    quilos: float
    data_producao: date


class ProducaoLeiteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    propriedade_id: UUID
    litros: float
    data_producao: date


class ProducaoCarneResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    propriedade_id: UUID
    quilos: float
    data_producao: date
