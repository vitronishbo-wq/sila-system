from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.resources.ambiente.domain.enums import (
    StatusEstudoAmbiental,
    TipoEstudoAmbiental,
)


class EstudoCreate(BaseModel):
    numero_licenca: str
    tipo: TipoEstudoAmbiental
    descricao: str
    responsavel_tecnico: str


class EstudoAprovacaoInput(BaseModel):
    analista_id: UUID


class EstudoComplementacaoInput(BaseModel):
    analista_id: UUID
    motivo: str


class EstudoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_estudo: str
    numero_licenca: str
    tipo: TipoEstudoAmbiental
    descricao: str
    responsavel_tecnico: str
    status: StatusEstudoAmbiental
    data_submissao: date
    data_analise: date | None = None
    data_aprovacao: date | None = None
    analista_id: UUID | None = None
    observacoes: str | None = None
