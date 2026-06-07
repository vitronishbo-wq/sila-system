from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID

from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import (
    CategoriaConsumo,
    StatusConsumo,
)


@dataclass
class ConsumoModel:
    id: UUID
    codigo_consumo: str
    abastecimento_id: UUID
    titular_id: UUID
    referencia: str
    categoria: CategoriaConsumo
    volume_m3: Decimal
    unidade_volume: str
    data_leitura: date
    status: StatusConsumo
    data_registro: date
