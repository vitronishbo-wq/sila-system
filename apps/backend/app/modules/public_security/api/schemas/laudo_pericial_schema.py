from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.public_security.domain.enums import StatusLaudo, TipoLaudo

class LaudoPericialCreate(BaseModel):
    prova_id: UUID
    tipo_laudo: TipoLaudo
    perito_id: UUID
    conclusao: str = Field(..., min_length=10)
    resumo: str | None = None
    arquivo_url: str | None = None
    observacoes: str | None = None
    citizen_id: UUID | None = None

class LaudoPericialStatusUpdate(BaseModel):
    status: StatusLaudo
    observacoes: str | None = None

class LaudoPericialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_laudo: str
    prova_id: UUID
    tipo_laudo: TipoLaudo
    perito_id: UUID
    data_emissao: date
    conclusao: str
    status: StatusLaudo
    resumo: str | None = None
    arquivo_url: str | None = None
    ativo: bool