from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.public_security.domain.enums import StatusProva, TipoProva


class ProvaPericialCreate(BaseModel):
    ocorrencia_id: UUID
    tipo: TipoProva
    descricao: str = Field(..., min_length=5)
    local_coleta: str
    data_coleta: date | None = None
    coletado_por_id: UUID | None = None
    observacoes: str | None = None
    citizen_id: UUID | None = None


class ProvaPericialStatusUpdate(BaseModel):
    status: StatusProva
    observacoes: str | None = None


class ProvaPericialVinculoCadeia(BaseModel):
    cadeia_custodia_id: UUID


class ProvaPericialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_prova: str
    ocorrencia_id: UUID
    tipo: TipoProva
    descricao: str
    data_coleta: date
    local_coleta: str
    status: StatusProva
    coletado_por_id: UUID | None = None
    cadeia_custodia_id: UUID | None = None
    ativo: bool
