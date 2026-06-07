from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from uuid import UUID

from apps.backend.app.modules.industry.domain.enums import (
    PorteIndustrial,
    RamoIndustrial,
    StatusEstabelecimento,
    TipoEstabelecimento,
)


@dataclass
class EstabelecimentoIndustrialModel:
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
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    audit_log: list[str] = field(default_factory=list)
    observacoes: str | None = None
