from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.resources.ambiente.domain.enums import StatusFiscalizacao

class FiscalizacaoCreate(BaseModel):
    numero_licenca: str
    localidade: str
    objetivo: str
    fiscal_responsavel: str
    data_agendada: date

class FiscalizacaoConclusaoInput(BaseModel):
    relatorio: str

class FiscalizacaoCancelamentoInput(BaseModel):
    motivo: str

class FiscalizacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_fiscalizacao: str
    numero_licenca: str
    localidade: str
    objetivo: str
    fiscal_responsavel: str
    status: StatusFiscalizacao
    data_agendada: date
    data_realizacao: date | None = None
    relatorio: str | None = None
    observacoes: str | None = None