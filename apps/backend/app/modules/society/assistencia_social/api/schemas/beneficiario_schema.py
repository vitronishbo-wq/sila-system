from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.society.assistencia_social.domain.enums import FaixaVulnerabilidade, SituacaoBeneficiario

class BeneficiarioCreate(BaseModel):
    citizen_id: UUID
    faixa_vulnerabilidade: FaixaVulnerabilidade
    cadastro_unico_id: UUID | None = None
    observacoes: str | None = None

class BeneficiarioMotivo(BaseModel):
    motivo: str | None = None

class BeneficiarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_registro: str
    citizen_id: UUID
    cadastro_unico_id: UUID | None
    faixa_vulnerabilidade: FaixaVulnerabilidade
    situacao: SituacaoBeneficiario
    data_cadastro: date
    observacoes: str | None
    ativo: bool