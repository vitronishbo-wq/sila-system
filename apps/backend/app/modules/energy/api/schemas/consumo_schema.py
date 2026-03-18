from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.energy.domain.enums import TipoLeituraEnergia

class ConsumoLeituraInput(BaseModel):
    unidade_consumidora_id: UUID
    leitura_kwh: Decimal
    data_leitura: datetime
    tipo_leitura: TipoLeituraEnergia = TipoLeituraEnergia.REAL
    classe_tarifaria: str
    cpf_titular: str
    medidor_id: UUID | None = None

class ConsumoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
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