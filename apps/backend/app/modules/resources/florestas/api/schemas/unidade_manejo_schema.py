from __future__ import annotations
from datetime import date
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.resources.florestas.domain.enums import TipoCicloCorte, TipoManejo

class UnidadeManejoCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    area_total_ha: Decimal = Field(..., gt=0)
    tipo_manejo: TipoManejo
    ciclo_corte: TipoCicloCorte
    operador_id: UUID
    imovel_id: UUID

class UnidadeManejoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_um: str
    nome: str
    area_total_ha: Decimal
    area_manejo_ha: Decimal
    area_preservacao_ha: Decimal
    tipo_manejo: TipoManejo
    ciclo_corte: TipoCicloCorte
    operador_id: UUID
    imovel_id: UUID
    data_criacao: date
    plano_manejo_id: Optional[UUID] = None
    licenca_id: Optional[UUID] = None