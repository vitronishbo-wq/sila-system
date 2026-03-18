from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.infrastructure.domain.enums import StatusEdital

class EditalCreate(BaseModel):
    titulo: str
    objeto: str
    licitacao_id: UUID
    data_publicacao: date
    data_abertura: date
    data_encerramento: date
    numero_edital: str | None = None

class EditalMotivoInput(BaseModel):
    motivo: str

class EditalRetificacaoInput(BaseModel):
    descricao: str

class EditalEncerramentoInput(BaseModel):
    data_encerramento: date | None = None

class EditalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_edital: str
    titulo: str
    objeto: str
    licitacao_id: UUID
    status: StatusEdital
    data_publicacao: date
    data_abertura: date
    data_encerramento: date
    data_cadastro: date
    versao: int
    data_atualizacao: date | None = None
    observacoes: str | None = None