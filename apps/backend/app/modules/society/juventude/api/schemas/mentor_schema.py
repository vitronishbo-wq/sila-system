from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.society.juventude.domain.enums import (
    AreaInteresse,
    StatusMentoria,
    TipoMentoria,
)


class MentorCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    tipo_mentoria: TipoMentoria
    area_interesse: AreaInteresse
    email: str | None = None
    telefone: str | None = None
    observacoes: str | None = None


class MentorStatusUpdate(BaseModel):
    status: StatusMentoria


class MentorAtribuirJovem(BaseModel):
    jovem_id: UUID


class MentorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_mentor: str
    nome: str
    tipo_mentoria: TipoMentoria
    area_interesse: AreaInteresse
    email: str | None = None
    telefone: str | None = None
    jovem_ids: list[UUID] | None = None
    status: StatusMentoria
    data_cadastro: date
    observacoes: str | None = None
    ativo: bool
