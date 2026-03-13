from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.society.juventude.domain.enums import TipoBolsa

class BolsaEstudoCreate(BaseModel):
    jovem_id: UUID
    tipo: TipoBolsa
    valor_mensal: Decimal = Field(..., gt=0)
    data_inicio: date
    data_fim: date | None = None
    observacoes: str | None = None

class BolsaEstudoEncerrar(BaseModel):
    observacoes: str | None = None

class BolsaEstudoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_bolsa: str
    jovem_id: UUID
    tipo: TipoBolsa
    valor_mensal: Decimal
    data_inicio: date
    data_fim: date | None = None
    data_cadastro: date
    observacoes: str | None = None
    ativa: bool