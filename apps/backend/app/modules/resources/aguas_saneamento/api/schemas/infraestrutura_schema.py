from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import StatusInfraestrutura, TipoInfraestrutura

class InfraestruturaCreate(BaseModel):
    tipo: TipoInfraestrutura
    nome: str
    provincia: str
    municipio: str
    capacidade: Decimal | None = None
    unidade_capacidade: str | None = None
    outorga_id: UUID | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None

class InfraestruturaMotivoInput(BaseModel):
    motivo: str

class InfraestruturaAtivacaoInput(BaseModel):
    data_operacao: date | None = None

class InfraestruturaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_infraestrutura: str
    tipo: TipoInfraestrutura
    nome: str
    provincia: str
    municipio: str
    status: StatusInfraestrutura
    data_registro: date
    capacidade: Decimal | None = None
    unidade_capacidade: str | None = None
    outorga_id: UUID | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    data_operacao: date | None = None
    observacoes: str | None = None