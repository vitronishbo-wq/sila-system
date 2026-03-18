from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.civil_protection.domain.enums import StatusAtendimento

class AtendimentoCreate(BaseModel):
    despacho_id: UUID
    local_atendimento: str = Field(..., min_length=3)
    vitimas_atendidas: int = Field(default=0, ge=0)
    desalojados_atendidos: int = Field(default=0, ge=0)
    obitos_confirmados: int = Field(default=0, ge=0)
    equipe_responsavel_id: UUID | None = None
    observacoes: str | None = None
    citizen_id: UUID | None = None

class AtendimentoStatusUpdate(BaseModel):
    status: StatusAtendimento
    observacoes: str | None = None

class AtendimentoFinalizacao(BaseModel):
    resumo: str | None = None
    observacoes: str | None = None

class AtendimentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_atendimento: str
    despacho_id: UUID
    ocorrencia_id: UUID
    status: StatusAtendimento
    inicio_atendimento: datetime
    fim_atendimento: datetime | None
    local_atendimento: str
    vitimas_atendidas: int
    desalojados_atendidos: int
    obitos_confirmados: int
    equipe_responsavel_id: UUID | None
    ativo: bool