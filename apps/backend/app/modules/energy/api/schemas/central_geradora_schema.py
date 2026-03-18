from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.energy.domain.enums import FonteEnergia, StatusInfraEnergia

class CentralGeradoraCreate(BaseModel):
    nome: str
    tipo: FonteEnergia
    capacidade_instalada_mw: Decimal
    municipio: str
    provincia: str

class CentralGeradoraDataInput(BaseModel):
    data: date

class CentralGeradoraResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    nome: str
    tipo: FonteEnergia
    capacidade_instalada_mw: Decimal
    municipio: str
    provincia: str
    status: StatusInfraEnergia
    data_inicio_construcao: date | None = None
    data_inicio_operacao: date | None = None