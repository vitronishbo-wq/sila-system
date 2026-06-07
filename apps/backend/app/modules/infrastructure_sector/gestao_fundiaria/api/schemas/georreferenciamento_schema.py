from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GeorreferenciamentoCreate(BaseModel):
    imovel_inscricao: str
    latitude: Decimal
    longitude: Decimal
    sistema_referencia: str = "WGS84"
    precisao_metros: Decimal | None = None
    area_calculada: Decimal | None = None
    codigo_geo: str | None = None


class GeorreferenciamentoPontoInput(BaseModel):
    latitude: Decimal
    longitude: Decimal


class GeorreferenciamentoMotivoInput(BaseModel):
    motivo: str


class GeorreferenciamentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_geo: str
    imovel_inscricao: str
    latitude: Decimal
    longitude: Decimal
    sistema_referencia: str
    data_registro: date
    precisao_metros: Decimal | None = None
    area_calculada: Decimal | None = None
    validado: bool
    ativo: bool
    data_atualizacao: date | None = None
    observacoes: str | None = None
