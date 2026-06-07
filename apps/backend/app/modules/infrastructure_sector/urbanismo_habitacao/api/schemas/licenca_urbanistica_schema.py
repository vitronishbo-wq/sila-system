from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import (
    StatusLicencaUrbanistica,
    TipoAlvara,
)


class LicencaUrbanisticaCreate(BaseModel):
    numero_processo: str
    tipo_alvara: TipoAlvara
    requerente_id: UUID
    zoneamento_id: UUID
    provincia: str
    municipio: str | None = None
    endereco_obra: str | None = None
    area_construida_prevista: Decimal | None = None
    codigo_licenca: str | None = None


class LicencaUrbanisticaDeferimentoInput(BaseModel):
    data_emissao: date
    data_validade: date
    tecnico_responsavel_id: UUID


class LicencaUrbanisticaMotivoInput(BaseModel):
    motivo: str


class LicencaUrbanisticaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_licenca: str
    numero_processo: str
    tipo_alvara: TipoAlvara
    status: StatusLicencaUrbanistica
    requerente_id: UUID
    zoneamento_id: UUID
    provincia: str
    municipio: str | None = None
    endereco_obra: str | None = None
    area_construida_prevista: Decimal | None = None
    data_requerimento: date
    data_emissao: date | None = None
    data_validade: date | None = None
    tecnico_responsavel_id: UUID | None = None
    observacoes: str | None = None
    data_atualizacao: date | None = None
