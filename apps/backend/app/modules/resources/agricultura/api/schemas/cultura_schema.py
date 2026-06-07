from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.resources.agricultura.domain.enums import TipoCultura


class CulturaCreate(BaseModel):
    nome: str
    tipo: TipoCultura
    ciclo_dias: int
    produtividade_estimada_ton_ha: float


class CulturaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_cultura: str
    nome: str
    tipo: TipoCultura
    ciclo_dias: int
    produtividade_estimada_ton_ha: float
    data_registro: date
    ativa: bool
