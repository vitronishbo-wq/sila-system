from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.resources.pescas.industrial.domain.enums import MercadoDestino, StatusLoteProducao

class LoteProducaoCreate(BaseModel):
    unidade_processamento_id: UUID
    produto_processado_id: UUID
    data_producao: date
    quantidade_kg: Decimal = Field(..., gt=0)
    destino_mercado: MercadoDestino
    data_validade: date | None = None
    turno: str | None = None
    temperatura_armazenamento_c: Decimal | None = None
    observacoes: str | None = None

class LoteProducaoUpdate(BaseModel):
    quantidade_kg: Decimal | None = Field(default=None, gt=0)
    status: StatusLoteProducao | None = None
    destino_mercado: MercadoDestino | None = None
    data_validade: date | None = None
    turno: str | None = None
    temperatura_armazenamento_c: Decimal | None = None
    observacoes: str | None = None

class LoteProducaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_lote: str
    unidade_processamento_id: UUID
    produto_processado_id: UUID
    data_producao: date
    quantidade_kg: Decimal
    status: StatusLoteProducao
    destino_mercado: MercadoDestino
    data_validade: date | None = None
    turno: str | None = None
    temperatura_armazenamento_c: Decimal | None = None
    observacoes: str | None = None