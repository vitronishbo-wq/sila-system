from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.resources.ambiente.domain.enums import StatusLicenca, TipoLicenca

class LicencaCreate(BaseModel):
    numero_car: str
    tipo: TipoLicenca
    atividade: str

class LicencaDeferimentoInput(BaseModel):
    analista_id: UUID
    data_validade: date
    condicionantes: list[str] | None = None

class LicencaIndeferimentoInput(BaseModel):
    analista_id: UUID
    motivo: str

class LicencaSuspensaoInput(BaseModel):
    motivo: str

class LicencaCancelamentoInput(BaseModel):
    motivo: str

class LicencaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_licenca: str
    numero_car: str
    tipo: TipoLicenca
    atividade: str
    status: StatusLicenca
    data_requerimento: date
    data_analise: date | None = None
    data_emissao: date | None = None
    data_validade: date | None = None
    analista_id: UUID | None = None
    condicionantes: list[str] | None = None
    observacoes: str | None = None