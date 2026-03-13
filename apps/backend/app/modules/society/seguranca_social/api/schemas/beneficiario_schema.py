from __future__ import annotations
from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.society.seguranca_social.domain.enums import EstadoBeneficiario, RegimeSegurancaSocial, TipoBeneficiario

class BeneficiarioCreate(BaseModel):
    citizen_id: UUID
    tipo: TipoBeneficiario
    regime: RegimeSegurancaSocial

class BeneficiarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_beneficiario: str
    citizen_id: UUID
    data_inscricao: date
    tipo: TipoBeneficiario
    regime: RegimeSegurancaSocial
    estado: EstadoBeneficiario
    data_ativacao: Optional[date] = None
    data_suspensao: Optional[date] = None
    data_cancelamento: Optional[date] = None
    motivo_cancelamento: Optional[str] = None
    observacoes: Optional[str] = None

class BeneficiarioFilter(BaseModel):
    tipo: Optional[TipoBeneficiario] = None
    estado: Optional[EstadoBeneficiario] = None
    regime: Optional[RegimeSegurancaSocial] = None