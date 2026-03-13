from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.civil_protection.domain.enums import StatusDespacho

class DespachoCreate(BaseModel):
    ocorrencia_id: UUID
    bombeiro_responsavel_id: UUID | None = None
    meio_deslocamento: str | None = None
    observacoes: str | None = None
    citizen_id: UUID | None = None

class DespachoStatusUpdate(BaseModel):
    status: StatusDespacho
    observacoes: str | None = None

class DespachoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_despacho: str
    ocorrencia_id: UUID
    corporacao_id: UUID
    bombeiro_responsavel_id: UUID | None
    status: StatusDespacho
    data_despacho: datetime
    data_ultima_atualizacao: datetime
    meio_deslocamento: str | None
    ativo: bool