from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.energy.domain.enums import StatusInfraEnergia


class LinhaTransmissaoCreate(BaseModel):
    origem_id: UUID
    origem_tipo: Literal["central_geradora", "subestacao"]
    destino_id: UUID
    destino_tipo: Literal["central_geradora", "subestacao"]
    capacidade_mw: Decimal
    extensao_km: Decimal


class LinhaTransmissaoDataInput(BaseModel):
    data: date


class LinhaTransmissaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    origem_id: UUID
    origem_tipo: str
    destino_id: UUID
    destino_tipo: str
    capacidade_mw: Decimal
    extensao_km: Decimal
    status: StatusInfraEnergia
    data_inicio_construcao: date | None = None
    data_inicio_operacao: date | None = None
