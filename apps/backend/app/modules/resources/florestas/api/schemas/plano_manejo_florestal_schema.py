from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.resources.florestas.domain.enums import StatusPlanoManejo


class PlanoManejoCreate(BaseModel):
    unidade_manejo_id: UUID
    responsavel_tecnico_id: UUID
    responsavel_tecnico_registro: str = Field(..., min_length=3)
    volume_anual_estimado_m3: Decimal = Field(..., gt=0)
    ciclo_corte_anos: int = Field(..., gt=0)
    area_anual_ha: Decimal = Field(..., gt=0)


class PlanoManejoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_pmfs: str
    unidade_manejo_id: UUID
    responsavel_tecnico_id: UUID
    responsavel_tecnico_registro: str
    status: StatusPlanoManejo
    data_submissao: date
    data_aprovacao: date | None = None
    data_validade: date | None = None
    volume_anual_estimado_m3: Decimal
    ciclo_corte_anos: int
    area_anual_ha: Decimal


PlanoManejoFlorestalCreate = PlanoManejoCreate
PlanoManejoFlorestalResponse = PlanoManejoResponse
