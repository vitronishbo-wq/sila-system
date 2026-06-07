from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.infrastructure_sector.aviacao_civil.domain.enums import (
    NaturezaVoo,
    RegrasVoo,
    StatusVoo,
    TipoVoo,
)


class VooCreate(BaseModel):
    numero_voo: str = Field(min_length=3, max_length=12)
    empresa_id: UUID
    aeronave_id: UUID
    aeroporto_origem_id: UUID
    aeroporto_destino_id: UUID
    data_hora_partida: datetime
    data_hora_chegada: datetime
    tipo: TipoVoo
    natureza: NaturezaVoo
    regras: RegrasVoo
    passageiros: int = Field(ge=0)
    tripulantes: list[dict] = Field(default_factory=list)


class VooStatusInput(BaseModel):
    data_hora: datetime


class VooResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_voo: str
    empresa_id: UUID
    aeronave_id: UUID
    aeroporto_origem_id: UUID
    aeroporto_destino_id: UUID
    data_hora_partida_programada: datetime
    data_hora_chegada_programada: datetime
    data_hora_partida_real: datetime | None
    data_hora_chegada_real: datetime | None
    tipo: TipoVoo
    natureza: NaturezaVoo
    regras: RegrasVoo
    passageiros: int
    status: StatusVoo
    tripulantes: list[dict]
