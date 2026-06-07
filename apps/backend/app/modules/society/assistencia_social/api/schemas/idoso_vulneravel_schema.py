from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.society.assistencia_social.domain.enums import StatusAcompanhamento


class IdosoVulneravelCreate(BaseModel):
    beneficiario_id: UUID
    citizen_id_idoso: UUID
    idade: int
    dependencia: bool
    precisa_cuidados: bool


class IdosoVulneravelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo: str
    beneficiario_id: UUID
    citizen_id_idoso: UUID
    idade: int
    dependencia: bool
    precisa_cuidados: bool
    data_registro: datetime
    status: StatusAcompanhamento
