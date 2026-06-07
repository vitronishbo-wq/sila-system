from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.society.assistencia_social.domain.enums import StatusAcompanhamento


class SituacaoRuaCreate(BaseModel):
    beneficiario_id: UUID
    localizacao: str
    motivo: str


class SituacaoRuaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo: str
    beneficiario_id: UUID
    data_registro: datetime
    localizacao: str
    motivo: str
    status: StatusAcompanhamento
