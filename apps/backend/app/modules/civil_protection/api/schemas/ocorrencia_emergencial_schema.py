from __future__ import annotations
from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.modules.civil_protection.domain.enums import PrioridadeAtendimento, StatusOcorrenciaEmergencial, TipoOcorrenciaEmergencial

class OcorrenciaEmergencialCreate(BaseModel):
    corporacao_id: UUID
    tipo: TipoOcorrenciaEmergencial
    prioridade: PrioridadeAtendimento
    data_ocorrencia: datetime
    descricao: str = Field(..., min_length=5)
    municipio: str
    provincia: str
    bombeiro_responsavel_id: UUID | None = None
    endereco: str | None = None
    vitimas: int = Field(default=0, ge=0)
    desalojados: int = Field(default=0, ge=0)
    obitos: int = Field(default=0, ge=0)
    observacoes: str | None = None
    citizen_id: UUID | None = None

class OcorrenciaEmergencialStatusUpdate(BaseModel):
    status: StatusOcorrenciaEmergencial
    observacoes: str | None = None

class OcorrenciaEmergencialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_ocorrencia: str
    corporacao_id: UUID
    tipo: TipoOcorrenciaEmergencial
    status: StatusOcorrenciaEmergencial
    prioridade: PrioridadeAtendimento
    data_ocorrencia: datetime
    data_registro: date
    municipio: str
    provincia: str
    vitimas: int
    desalojados: int
    obitos: int
    ativo: bool