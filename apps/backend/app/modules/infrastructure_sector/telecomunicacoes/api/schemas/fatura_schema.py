from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import (
    StatusFaturaTelecom,
)


class FaturaGerarInput(BaseModel):
    referencia: str = Field(min_length=4, max_length=20)
    consumo_total_gb: Decimal = Field(ge=0)


class FaturaTelecomResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_fatura: str
    assinante_id: UUID
    referencia: str
    consumo_total_gb: Decimal
    franquia_gb: Decimal
    excedente_gb: Decimal
    valor_plano: Decimal
    valor_excedente: Decimal
    valor_total: Decimal
    data_emissao: date
    data_vencimento: date
    status: StatusFaturaTelecom
