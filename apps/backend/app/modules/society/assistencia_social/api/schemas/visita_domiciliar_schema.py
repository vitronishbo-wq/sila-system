from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.society.assistencia_social.domain.enums import ResultadoVisita

class VisitaDomiciliarCreate(BaseModel):
    beneficiario_id: UUID
    assistente_social_id: UUID
    condicoes_moradia: str
    observacoes: str | None = None
    recomendacoes: list[str] | None = None
    resultado: ResultadoVisita = ResultadoVisita.RETORNO_NECESSARIO

class VisitaDomiciliarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo: str
    beneficiario_id: UUID
    assistente_social_id: UUID
    data_visita: datetime
    condicoes_moradia: str
    observacoes: str | None
    recomendacoes: list[str]
    resultado: ResultadoVisita