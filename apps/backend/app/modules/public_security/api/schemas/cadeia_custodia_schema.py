from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.public_security.domain.enums import StatusCadeiaCustodia

class CadeiaCustodiaCreate(BaseModel):
    prova_id: UUID
    local_atual: str
    responsavel_id: UUID
    observacoes: str | None = None
    citizen_id: UUID | None = None

class CadeiaCustodiaMovimentacao(BaseModel):
    status: StatusCadeiaCustodia
    local_atual: str
    responsavel_id: UUID
    observacao: str | None = None

class CadeiaCustodiaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_cadeia: str
    prova_id: UUID
    ocorrencia_id: UUID
    status: StatusCadeiaCustodia
    local_atual: str
    responsavel_id: UUID
    data_inicio: datetime
    data_ultima_movimentacao: datetime
    integridade_verificada: bool
    ativo: bool