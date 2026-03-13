from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.society.assistencia_social.domain.enums import StatusBeneficio, TipoBeneficio

class BeneficioCreate(BaseModel):
    beneficiario_id: UUID
    tipo: TipoBeneficio
    valor: Decimal
    programa_social_id: UUID | None = None

class BeneficioBpcPcdCreate(BaseModel):
    beneficiario_id: UUID
    pcd_id: UUID
    valor: Decimal

class BeneficioMotivo(BaseModel):
    motivo: str

class BeneficioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo: str
    beneficiario_id: UUID
    programa_social_id: UUID | None
    tipo: TipoBeneficio
    valor: Decimal
    status: StatusBeneficio
    data_solicitacao: date
    data_concessao: date | None
    data_fim: date | None
    motivo_status: str | None