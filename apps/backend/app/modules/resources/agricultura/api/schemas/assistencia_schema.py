from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.resources.agricultura.domain.enums import StatusAssistencia

class AssistenciaCreate(BaseModel):
    codigo_propriedade: str
    tecnico_nome: str
    objetivo: str

class AssistenciaConclusaoInput(BaseModel):
    recomendacoes: str | None = None

class AssistenciaCancelamentoInput(BaseModel):
    motivo: str

class AssistenciaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_assistencia: str
    codigo_propriedade: str
    tecnico_nome: str
    objetivo: str
    status: StatusAssistencia
    data_agendamento: date
    data_realizacao: date | None = None
    recomendacoes: str | None = None
    motivo_cancelamento: str | None = None