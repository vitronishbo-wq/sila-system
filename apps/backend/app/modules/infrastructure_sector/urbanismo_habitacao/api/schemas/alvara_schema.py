from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusAlvara, TipoAlvara

class AlvaraCreate(BaseModel):
    numero_processo: str
    tipo: TipoAlvara
    licenca_urbanistica_id: UUID
    requerente_id: UUID
    provincia: str
    municipio: str | None = None
    endereco_obra: str | None = None
    area_autorizada: Decimal | None = None
    codigo_alvara: str | None = None

class AlvaraDeferimentoInput(BaseModel):
    data_emissao: date
    data_validade: date
    analista_id: UUID

class AlvaraMotivoInput(BaseModel):
    motivo: str

class AlvaraResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_alvara: str
    numero_processo: str
    tipo: TipoAlvara
    status: StatusAlvara
    licenca_urbanistica_id: UUID
    requerente_id: UUID
    provincia: str
    municipio: str | None = None
    endereco_obra: str | None = None
    area_autorizada: Decimal | None = None
    data_requerimento: date
    data_emissao: date | None = None
    data_validade: date | None = None
    analista_id: UUID | None = None
    observacoes: str | None = None
    data_atualizacao: date | None = None