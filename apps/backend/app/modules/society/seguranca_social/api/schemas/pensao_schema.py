from __future__ import annotations
from datetime import date
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.modules.society.seguranca_social.domain.enums import Periodicidade, StatusPensao, TipoPensao

class PensaoCreate(BaseModel):
    beneficiario_id: UUID
    tipo: TipoPensao
    valor_mensal: Decimal = Field(..., gt=0)
    conta_bancaria: Optional[str] = None
    iban: Optional[str] = None

class PensaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_processo: str
    beneficiario_id: UUID
    tipo: TipoPensao
    data_inicio: date
    valor_mensal: Decimal
    periodicidade: Periodicidade
    status: StatusPensao
    data_fim: Optional[date] = None
    conta_bancaria: Optional[str] = None
    iban: Optional[str] = None
    observacoes: Optional[str] = None

class PensaoFilter(BaseModel):
    beneficiario_id: Optional[UUID] = None
    tipo: Optional[TipoPensao] = None
    status: Optional[StatusPensao] = None

class PensaoAction(BaseModel):
    actor_id: UUID

class PensaoMotivo(BaseModel):
    motivo: str = Field(..., min_length=3, max_length=500)