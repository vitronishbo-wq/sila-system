from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.energy.domain.enums import TipoLeituraEnergia

@dataclass
class ConsumoEnergiaModel:
    id: UUID
    unidade_consumidora_id: UUID
    medidor_id: UUID | None
    data_leitura: datetime
    leitura_kwh: Decimal
    leitura_anterior_kwh: Decimal | None
    consumo_periodo_kwh: Decimal
    tipo_leitura: TipoLeituraEnergia
    classe_tarifaria: str
    cpf_titular: str