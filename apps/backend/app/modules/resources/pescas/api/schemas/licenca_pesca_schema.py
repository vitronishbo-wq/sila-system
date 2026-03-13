from __future__ import annotations
from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.resources.pescas.domain.enums import StatusLicenca

class LicencaPescaCreate(BaseModel):
    embarcacao_id: UUID
    titular_id: UUID
    modalidade_autorizada: str
    zona_pesca_id: UUID
    validade_dias: int = 365

class LicencaPescaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_licenca: str
    embarcacao_id: UUID
    titular_id: UUID
    data_emissao: date
    data_validade: date
    status: StatusLicenca
    modalidade_autorizada: str
    zona_pesca_id: UUID
    observacoes: Optional[str] = None