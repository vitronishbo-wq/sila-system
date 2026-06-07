from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.society.seguranca_social.domain.enums import (
    EstadoBeneficiario,
    RegimeSegurancaSocial,
    TipoBeneficiario,
)


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
    data_ativacao: date | None = None
    data_suspensao: date | None = None
    data_cancelamento: date | None = None
    motivo_cancelamento: str | None = None
    observacoes: str | None = None


class BeneficiarioFilter(BaseModel):
    tipo: TipoBeneficiario | None = None
    estado: EstadoBeneficiario | None = None
    regime: RegimeSegurancaSocial | None = None
