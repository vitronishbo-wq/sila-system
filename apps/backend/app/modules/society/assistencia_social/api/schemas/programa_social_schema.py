from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.society.assistencia_social.domain.enums import PublicoAlvo, StatusProgramaSocial

class ProgramaSocialCreate(BaseModel):
    nome: str
    publico_alvo: PublicoAlvo
    criterio_renda_max: Decimal
    valor_base: Decimal
    vagas: int | None = None
    data_inicio: date
    observacoes: str | None = None

class ProgramaSocialSuspender(BaseModel):
    motivo: str | None = None

class ProgramaSocialEncerrar(BaseModel):
    data_fim: date
    motivo: str | None = None

class ProgramaSocialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo: str
    nome: str
    publico_alvo: PublicoAlvo
    criterio_renda_max: Decimal
    valor_base: Decimal
    vagas: int | None
    status: StatusProgramaSocial
    data_inicio: date
    data_fim: date | None
    observacoes: str | None