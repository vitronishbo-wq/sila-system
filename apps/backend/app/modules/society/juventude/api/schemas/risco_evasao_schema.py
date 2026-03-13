from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.society.juventude.domain.enums import RiscoSocial, SituacaoOcupacional, TipoVulnerabilidade

class RiscoEvasaoAvaliar(BaseModel):
    jovem_id: UUID
    observacoes: str | None = None

class RiscoEvasaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_risco: str
    jovem_id: UUID
    citizen_id: UUID | None
    matricula_ativa: bool
    situacao_ocupacional: SituacaoOcupacional
    vulnerabilidades: list[TipoVulnerabilidade] | None = None
    pontuacao: int
    nivel_risco: RiscoSocial
    data_avaliacao: date
    fatores: list[str]
    recomendacoes: list[str]
    observacoes: str | None = None
    ativo: bool