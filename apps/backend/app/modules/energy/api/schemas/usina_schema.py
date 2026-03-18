from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.energy.domain.enums import FonteEnergia, StatusUsina, TipoUsina

class UsinaCreate(BaseModel):
    codigo_aneel: str
    nome: str
    fonte: FonteEnergia
    tipo: TipoUsina
    potencia_instalada_mw: Decimal
    proprietario_id: UUID
    proprietario_tipo: str
    municipio: str
    provincia: str

class UsinaDataInput(BaseModel):
    data: date

class UsinaMotivoInput(BaseModel):
    motivo: str

class UsinaPotenciaInput(BaseModel):
    potencia: Decimal

class UsinaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_aneel: str
    nome: str
    fonte: FonteEnergia
    tipo: TipoUsina
    status: StatusUsina
    potencia_instalada_mw: Decimal
    proprietario_id: UUID
    proprietario_tipo: str
    municipio: str
    provincia: str
    potencia_fiscalizada_mw: Decimal | None = None
    data_inicio_construcao: date | None = None
    data_entrada_operacao: date | None = None
    observacoes: str | None = None