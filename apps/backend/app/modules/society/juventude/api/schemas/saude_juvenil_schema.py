from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.modules.society.juventude.domain.enums import StatusAcompanhamento, TipoSaudeJuvenil

class SaudeJuvenilCreate(BaseModel):
    jovem_id: UUID
    tipo_registo: TipoSaudeJuvenil
    descricao: str = Field(..., min_length=3)
    data_registo: date
    encaminhamento_necessario: bool = False
    observacoes: str | None = None

class SaudeJuvenilStatusUpdate(BaseModel):
    status: StatusAcompanhamento

class SaudeJuvenilResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_registo: str
    jovem_id: UUID
    tipo_registo: TipoSaudeJuvenil
    descricao: str
    data_registo: date
    status_acompanhamento: StatusAcompanhamento
    encaminhamento_necessario: bool
    data_cadastro: date
    observacoes: str | None = None
    ativo: bool