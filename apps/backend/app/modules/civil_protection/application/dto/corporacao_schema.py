from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.civil_protection.domain.enums import StatusCorporacao


class CorporacaoCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    municipio: str
    provincia: str
    endereco: str
    comandante: str
    telefone: str | None = None
    email: str | None = None
    observacoes: str | None = None
    citizen_id: UUID | None = None


class CorporacaoStatusUpdate(BaseModel):
    status: StatusCorporacao
    motivo: str | None = None


class CorporacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_corporacao: str
    nome: str
    municipio: str
    provincia: str
    comandante: str
    data_ativacao: date
    status: StatusCorporacao
    ativo: bool
