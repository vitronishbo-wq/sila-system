from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.energy.domain.enums import StatusInfraEnergia

@dataclass
class LinhaTransmissaoModel:
    id: UUID
    origem_id: UUID
    origem_tipo: str
    destino_id: UUID
    destino_tipo: str
    capacidade_mw: Decimal
    extensao_km: Decimal
    status: StatusInfraEnergia
    data_inicio_construcao: date | None = None
    data_inicio_operacao: date | None = None