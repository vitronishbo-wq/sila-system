from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.industry.domain.enums import (
    PorteIndustrial,
    RamoIndustrial,
    StatusEstabelecimento,
    TipoEstabelecimento,
)


class EstabelecimentoIndustrialCreate(BaseModel):
    cnpj: str
    razao_social: str
    ramo: RamoIndustrial
    porte: PorteIndustrial
    tipo: TipoEstabelecimento
    cnae_principal: str
    data_abertura: date
    endereco: str
    bairro: str
    municipio: str
    provincia: str


class DataInput(BaseModel):
    data: date


class MotivoInput(BaseModel):
    motivo: str


class RamoInput(BaseModel):
    ramo: RamoIndustrial


class PorteInput(BaseModel):
    porte: PorteIndustrial


class EstabelecimentoIndustrialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    cnpj: str
    razao_social: str
    ramo: RamoIndustrial
    porte: PorteIndustrial
    tipo: TipoEstabelecimento
    cnae_principal: str
    data_abertura: date
    endereco: str
    bairro: str
    municipio: str
    provincia: str
    status: StatusEstabelecimento
    nome_fantasia: str | None = None
    inscricao_estadual: str | None = None
    inscricao_municipal: str | None = None
    telefone: str | None = None
    email: str | None = None
    data_inicio_atividades: date | None = None
    data_encerramento: date | None = None
    licenca_operacao_id: UUID | None = None
    licenca_ambiental_id: UUID | None = None
    alvara_id: UUID | None = None
    created_at: datetime
    updated_at: datetime
    audit_log: list[str] = Field(default_factory=list)
    observacoes: str | None = None
