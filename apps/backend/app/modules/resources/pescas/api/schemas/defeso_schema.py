from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.resources.pescas.domain.enums import PeriodoDefesoTipo


class DefesoCreate(BaseModel):
    periodo: PeriodoDefesoTipo
    especie_id: UUID
    data_inicio: date
    data_fim: date


class DefesoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    periodo: PeriodoDefesoTipo
    especie_id: UUID
    data_inicio: date
    data_fim: date
    ativo: bool
