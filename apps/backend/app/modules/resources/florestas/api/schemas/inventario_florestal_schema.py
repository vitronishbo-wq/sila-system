from __future__ import annotations
from datetime import date
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class InventarioFlorestalCreate(BaseModel):
    unidade_manejo_id: UUID
    volume_estimado_m3: Decimal = Field(..., gt=0)
    area_inventariada_ha: Decimal = Field(..., gt=0)
    observacoes: Optional[str] = None

class InventarioFlorestalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    unidade_manejo_id: UUID
    data_inventario: date
    volume_estimado_m3: Decimal
    area_inventariada_ha: Decimal
    status: str
    observacoes: Optional[str] = None