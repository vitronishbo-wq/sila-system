from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.educacao.domain.models import CicloEnsino, TipoEscola


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
