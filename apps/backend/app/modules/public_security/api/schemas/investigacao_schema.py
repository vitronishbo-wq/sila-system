from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.public_security.domain.enums import StatusInvestigacao

class InvestigacaoCreate(BaseModel):
    ocorrencia_id: UUID
    delegado_responsavel_id: UUID | None = None
    resumo: str | None = None
    observacoes: str | None = None
    citizen_id: UUID | None = None

class InvestigacaoStatusUpdate(BaseModel):
    status: StatusInvestigacao
    observacoes: str | None = None

class InvestigacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_investigacao: str
    ocorrencia_id: UUID
    unidade_id: UUID
    data_abertura: date
    status: StatusInvestigacao
    delegado_responsavel_id: UUID | None = None
    data_conclusao: date | None = None
    resumo: str | None = None
    ativo: bool