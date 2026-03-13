from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.resources.aguas_saneamento.domain.enums import CategoriaConsumo, StatusConsumo

class ConsumoCreate(BaseModel):
    abastecimento_id: UUID
    titular_id: UUID
    referencia: str
    categoria: CategoriaConsumo
    volume_m3: Decimal
    unidade_volume: str
    hidrometro_id: UUID | None = None
    leitura_anterior: Decimal | None = None
    leitura_atual: Decimal | None = None
    data_leitura: date | None = None

class ConsumoMotivoInput(BaseModel):
    motivo: str

class ConsumoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
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
    hidrometro_id: UUID | None = None
    leitura_anterior: Decimal | None = None
    leitura_atual: Decimal | None = None
    observacoes: str | None = None