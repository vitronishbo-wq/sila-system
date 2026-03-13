from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.society.juventude.domain.enums import StatusBeneficio, TipoAuxilio

class AuxilioCreate(BaseModel):
    jovem_id: UUID
    tipo: TipoAuxilio
    data_inicio: date
    valor_mensal: Decimal | None = Field(default=None, ge=0)
    data_fim: date | None = None
    observacoes: str | None = None

class AuxilioStatusUpdate(BaseModel):
    status: StatusBeneficio
    observacoes: str | None = None

class AuxilioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_auxilio: str
    jovem_id: UUID
    tipo: TipoAuxilio
    data_inicio: date
    data_fim: date | None = None
    valor_mensal: Decimal | None = None
    status: StatusBeneficio
    data_cadastro: date
    observacoes: str | None = None
    ativo: bool