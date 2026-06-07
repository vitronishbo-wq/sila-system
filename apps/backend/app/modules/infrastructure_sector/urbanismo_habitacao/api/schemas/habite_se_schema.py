from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import (
    StatusHabiteSe,
    TipoHabiteSe,
)


class HabiteSeCreate(BaseModel):
    numero_processo: str
    tipo: TipoHabiteSe
    alvara_id: UUID
    requerente_id: UUID
    provincia: str
    municipio: str | None = None
    endereco_imovel: str | None = None
    area_vistoriada: Decimal | None = None
    codigo_habite_se: str | None = None


class HabiteSeVistoriaInput(BaseModel):
    data_vistoria: date
    tecnico_vistoriador_id: UUID


class HabiteSeEmissaoInput(BaseModel):
    data_emissao: date
    data_validade: date | None = None


class HabiteSeMotivoInput(BaseModel):
    motivo: str


class HabiteSeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_habite_se: str
    numero_processo: str
    tipo: TipoHabiteSe
    status: StatusHabiteSe
    alvara_id: UUID
    requerente_id: UUID
    provincia: str
    municipio: str | None = None
    endereco_imovel: str | None = None
    area_vistoriada: Decimal | None = None
    data_requerimento: date
    data_vistoria: date | None = None
    data_emissao: date | None = None
    data_validade: date | None = None
    tecnico_vistoriador_id: UUID | None = None
    observacoes: str | None = None
    data_atualizacao: date | None = None
