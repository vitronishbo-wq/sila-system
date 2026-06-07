from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID

from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import (
    StatusInfraestrutura,
    TipoInfraestrutura,
)


@dataclass
class InfraestruturaModel:
    id: UUID
    codigo_infraestrutura: str
    tipo: TipoInfraestrutura
    nome: str
    provincia: str
    municipio: str
    status: StatusInfraestrutura
    data_registro: date
    capacidade: Decimal | None
    unidade_capacidade: str | None
    outorga_id: UUID | None
    latitude: Decimal | None
    longitude: Decimal | None
