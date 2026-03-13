from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.resources.ambiente.domain.enums import StatusCondicionante

class CondicionanteCreate(BaseModel):
    numero_licenca: str
    descricao: str
    prazo_dias: int

class CondicionanteCumprimentoInput(BaseModel):
    evidencia: str | None = None

class CondicionanteDescumprimentoInput(BaseModel):
    motivo: str

class CondicionanteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_condicionante: str
    numero_licenca: str
    descricao: str
    prazo_dias: int
    status: StatusCondicionante
    data_criacao: date
    data_limite: date
    data_cumprimento: date | None = None
    evidencia: str | None = None
    observacoes: str | None = None