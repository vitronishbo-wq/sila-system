from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.modules.public_security.domain.enums import CargoPolicial, Patente, StatusAgente, TipoAgente, TipoVinculo

class PolicialCreate(BaseModel):
    unidade_id: UUID
    nome: str = Field(..., min_length=3)
    data_nascimento: date
    cpf: str = Field(..., pattern='^\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}$')
    rg: str
    tipo: TipoAgente
    vinculo: TipoVinculo
    cargo: CargoPolicial | None = None
    patente: Patente | None = None
    telefone: str | None = None
    email: str | None = None
    endereco: str | None = None
    observacoes: str | None = None
    citizen_id: UUID | None = None

class PolicialStatusUpdate(BaseModel):
    status: StatusAgente
    motivo: str | None = None

class PolicialPorteUpdate(BaseModel):
    numero_porte: str
    data_validade: date

class PolicialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    matricula: str
    unidade_id: UUID
    nome: str
    data_nascimento: date
    cpf: str
    tipo: TipoAgente
    vinculo: TipoVinculo
    cargo: CargoPolicial | None = None
    patente: Patente | None = None
    status: StatusAgente
    porte_arma: bool
    numero_porte: str | None = None
    data_validade_porte: date | None = None
    ativo: bool