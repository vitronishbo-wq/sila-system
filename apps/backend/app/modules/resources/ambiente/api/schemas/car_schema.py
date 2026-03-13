from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.resources.ambiente.domain.enums import Bioma, StatusCAR, TipoImovel

class ProprietarioCreate(BaseModel):
    nome: str
    documento: str
    telefone: str | None = None
    email: str | None = None

class ProprietarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_proprietario: str
    nome: str
    documento: str
    telefone: str | None = None
    email: str | None = None
    data_cadastro: date
    ativo: bool

class ImovelCreate(BaseModel):
    proprietario_id: UUID
    nome: str
    provincia: str
    municipio: str
    area_total: Decimal
    bioma: Bioma
    tipo_imovel: TipoImovel
    coordenadas: str | None = None

class ImovelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_imovel: str
    proprietario_id: UUID
    nome: str
    provincia: str
    municipio: str
    area_total: Decimal
    bioma: Bioma
    tipo_imovel: TipoImovel
    coordenadas: str | None = None
    data_cadastro: date
    ativo: bool

class CARCreate(BaseModel):
    imovel_id: UUID
    proprietario_id: UUID
    area_total: Decimal
    bioma: Bioma
    tipo_imovel: TipoImovel

class CARAreasInput(BaseModel):
    area_preservacao_permanente: Decimal
    area_reserva_legal: Decimal
    area_uso_alternativo: Decimal
    area_consolidada: Decimal

class CARAprovacaoInput(BaseModel):
    analista_id: UUID

class CARPendenciaInput(BaseModel):
    analista_id: UUID
    motivo: str

class CARResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_car: str
    imovel_id: UUID
    proprietario_id: UUID
    area_total: Decimal
    area_preservacao_permanente: Decimal
    area_reserva_legal: Decimal
    area_uso_alternativo: Decimal
    area_consolidada: Decimal
    bioma: Bioma
    tipo_imovel: TipoImovel
    status: StatusCAR
    data_cadastro: date
    data_analise: date | None = None
    data_aprovacao: date | None = None
    analista_id: UUID | None = None
    observacoes: str | None = None