from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.society.assistencia_social.domain.enums import StatusAcompanhamento


class PCDCreate(BaseModel):
    beneficiario_id: UUID
    citizen_id_pcd: UUID
    tipo_deficiencia: str
    cid: str
    grau_deficiencia: str
    laudo_id: UUID


class PCDResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo: str
    beneficiario_id: UUID
    citizen_id_pcd: UUID
    tipo_deficiencia: str
    cid: str
    grau_deficiencia: str
    laudo_id: UUID
    bpc_ativo: bool
    data_registro: datetime
    status: StatusAcompanhamento
