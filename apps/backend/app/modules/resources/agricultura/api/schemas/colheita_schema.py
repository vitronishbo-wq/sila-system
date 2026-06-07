from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ColheitaCreate(BaseModel):
    codigo_safra: str
    codigo_talhao: str
    quantidade_colhida_ton: float
    perdas_ton: float = 0.0
    umidade_percentual: float | None = None
    observacoes: str | None = None


class ColheitaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_colheita: str
    codigo_safra: str
    codigo_talhao: str
    quantidade_colhida_ton: float
    perdas_ton: float
    quantidade_liquida_ton: float
    data_colheita: date
    umidade_percentual: float | None = None
    observacoes: str | None = None
