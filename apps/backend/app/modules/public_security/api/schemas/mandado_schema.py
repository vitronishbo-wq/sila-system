from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.modules.public_security.domain.enums import StatusMandado, TipoMandado

class MandadoCreate(BaseModel):
    ocorrencia_id: UUID
    tipo: TipoMandado
    autoridade_judicial: str = Field(..., min_length=3)
    data_expedicao: date
    data_validade: date
    unidade_id: UUID | None = None
    policial_responsavel_id: UUID | None = None
    observacoes: str | None = None
    citizen_id: UUID | None = None

class MandadoStatusUpdate(BaseModel):
    status: StatusMandado
    observacoes: str | None = None

class MandadoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_mandado: str
    ocorrencia_id: UUID
    tipo: TipoMandado
    autoridade_judicial: str
    data_expedicao: date
    data_validade: date
    status: StatusMandado
    unidade_id: UUID | None = None
    policial_responsavel_id: UUID | None = None
    ativo: bool