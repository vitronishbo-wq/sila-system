from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4

@dataclass
class InventarioFlorestal:
    id: UUID
    unidade_manejo_id: UUID
    data_inventario: date
    volume_estimado_m3: Decimal
    area_inventariada_ha: Decimal
    status: str = 'aberto'
    observacoes: Optional[str] = None

    @classmethod
    def registrar(cls, *, unidade_manejo_id: UUID, volume_estimado_m3: Decimal, area_inventariada_ha: Decimal, observacoes: Optional[str]=None) -> 'InventarioFlorestal':
        return cls(id=uuid4(), unidade_manejo_id=unidade_manejo_id, data_inventario=date.today(), volume_estimado_m3=volume_estimado_m3, area_inventariada_ha=area_inventariada_ha, observacoes=observacoes)