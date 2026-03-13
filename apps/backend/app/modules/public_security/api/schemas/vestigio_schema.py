from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.public_security.domain.enums import StatusVestigio, TipoVestigio

class VestigioCreate(BaseModel):
    cadeia_custodia_id: UUID
    tipo: TipoVestigio
    descricao: str = Field(..., min_length=5)
    localizacao: str = Field(..., min_length=3)
    coletado_por_id: UUID | None = None
    observacoes: str | None = None
    citizen_id: UUID | None = None

class VestigioStatusUpdate(BaseModel):
    status: StatusVestigio
    observacoes: str | None = None

class VestigioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_vestigio: str
    cadeia_custodia_id: UUID
    ocorrencia_id: UUID
    tipo: TipoVestigio
    descricao: str
    localizacao: str
    data_coleta: datetime
    status: StatusVestigio
    coletado_por_id: UUID | None = None
    ativo: bool