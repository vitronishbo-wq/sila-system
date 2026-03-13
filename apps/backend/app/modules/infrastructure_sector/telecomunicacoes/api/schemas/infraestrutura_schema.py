from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusInfraestrutura, TipoInfraestrutura

class InfraestruturaCreate(BaseModel):
    operadora_id: UUID
    tipo: TipoInfraestrutura
    identificador: str
    municipio: str
    provincia: str
    data_implantacao: date
    latitude: float | None = None
    longitude: float | None = None
    capacidade: str | None = None
    observacoes: str | None = None

class InfraestruturaStatusUpdate(BaseModel):
    status: StatusInfraestrutura

class InfraestruturaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_infra: str
    operadora_id: UUID
    tipo: TipoInfraestrutura
    identificador: str
    municipio: str
    provincia: str
    data_implantacao: date
    status: StatusInfraestrutura
    latitude: float | None = None
    longitude: float | None = None
    capacidade: str | None = None
    ativo: bool