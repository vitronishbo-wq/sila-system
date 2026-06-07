from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.society.assistencia_social.domain.enums import (
    StatusAcompanhamento,
    TipoAtendimento,
)


class AtendimentoCreate(BaseModel):
    beneficiario_id: UUID
    tipo: TipoAtendimento
    descricao: str
    responsavel_id: UUID
    encaminhamentos: list[dict] | None = None


class AtendimentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo: str
    beneficiario_id: UUID
    tipo: TipoAtendimento
    descricao: str
    responsavel_id: UUID
    data_atendimento: datetime
    status: StatusAcompanhamento
    encaminhamentos: list[dict]
