from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusOutorga, TipoOutorga

class OutorgaEspectroCreate(BaseModel):
    operadora_id: UUID
    tipo_outorga: TipoOutorga
    faixa_inicio_mhz: float = Field(..., ge=0)
    faixa_fim_mhz: float = Field(..., gt=0)
    data_outorga: date
    data_validade: date | None = None
    observacoes: str | None = None

class OutorgaEspectroStatusUpdate(BaseModel):
    status: StatusOutorga

class OutorgaEspectroResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_outorga: str
    operadora_id: UUID
    tipo_outorga: TipoOutorga
    faixa_inicio_mhz: float
    faixa_fim_mhz: float
    data_outorga: date
    data_validade: date | None = None
    status: StatusOutorga
    ativo: bool