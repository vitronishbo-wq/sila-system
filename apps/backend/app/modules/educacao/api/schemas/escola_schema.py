from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.educacao.domain.models import CicloEnsino, TipoEscola


class EscolaCreate(BaseModel):
    codigo_med: str = Field(..., max_length=32)
    nome: str = Field(..., max_length=255)
    tipo: TipoEscola
    ciclos: list[CicloEnsino] = Field(default_factory=list)
    provincia: str = Field(..., max_length=128)
    municipio: str = Field(..., max_length=128)
    comuna: str = Field(..., max_length=128)
    bairro: str = Field(..., max_length=128)
    endereco: str
    contacto: str | None = Field(None, max_length=64)
    email: str | None = Field(None, max_length=255)


class EscolaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_med: str
    nome: str
    tipo: TipoEscola
    ciclos: list[CicloEnsino]
    provincia: str
    municipio: str
    comuna: str
    bairro: str
    endereco: str
    contacto: str | None = None
    email: str | None = None
    ativa: bool
