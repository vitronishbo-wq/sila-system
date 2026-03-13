from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusReclamacaoTelecom, TipoReclamacaoTelecom

class ReclamacaoCreate(BaseModel):
    assinante_id: UUID
    tipo: TipoReclamacaoTelecom
    descricao: str = Field(min_length=5)
    prioridade: str = Field(default='media', min_length=3, max_length=20)

class ReclamacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    protocolo: str
    assinante_id: UUID
    tipo: TipoReclamacaoTelecom
    descricao: str
    prioridade: str
    status: StatusReclamacaoTelecom
    data_abertura: datetime
    data_fechamento: datetime | None = None
    resposta: str | None = None