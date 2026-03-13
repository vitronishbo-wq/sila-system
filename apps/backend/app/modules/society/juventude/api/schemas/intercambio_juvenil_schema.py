from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.society.juventude.domain.enums import AreaInteresse, StatusIntercambio

class IntercambioJuvenilCreate(BaseModel):
    jovem_id: UUID
    pais_destino: str = Field(..., min_length=2)
    instituicao_destino: str = Field(..., min_length=3)
    area_interesse: AreaInteresse
    data_inicio: date
    data_fim: date | None = None
    observacoes: str | None = None

class IntercambioJuvenilStatusUpdate(BaseModel):
    status: StatusIntercambio

class IntercambioJuvenilResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_intercambio: str
    jovem_id: UUID
    pais_destino: str
    instituicao_destino: str
    area_interesse: AreaInteresse
    data_inicio: date
    data_fim: date | None = None
    status: StatusIntercambio
    data_cadastro: date
    observacoes: str | None = None
    ativo: bool