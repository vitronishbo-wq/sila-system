from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.energy.domain.enums import ClasseTensao, StatusInfraEnergia


class SubestacaoCreate(BaseModel):
    nome: str
    tensao_nominal_kv: Decimal
    classe_tensao: ClasseTensao
    municipio: str
    provincia: str


class SubestacaoDataInput(BaseModel):
    data: date


class SubestacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    nome: str
    tensao_nominal_kv: Decimal
    classe_tensao: ClasseTensao
    municipio: str
    provincia: str
    status: StatusInfraEnergia
    data_inicio_construcao: date | None = None
    data_inicio_operacao: date | None = None
