from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.society.assistencia_social.domain.enums import StatusAcompanhamento

class CriancaRiscoCreate(BaseModel):
    beneficiario_id: UUID
    citizen_id_crianca: UUID
    idade: int
    motivo: str
    escolarizada: bool

class CriancaRiscoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo: str
    beneficiario_id: UUID
    citizen_id_crianca: UUID
    idade: int
    motivo: str
    escolarizada: bool
    data_registro: datetime
    status: StatusAcompanhamento