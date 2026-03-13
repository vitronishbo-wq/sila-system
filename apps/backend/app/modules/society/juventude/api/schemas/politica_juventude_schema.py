from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.society.juventude.domain.enums import AreaInteresse, StatusPoliticaJuventude

class PoliticaJuventudeCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    descricao: str = Field(..., min_length=10)
    area_interesse: AreaInteresse
    data_inicio: date
    metas: dict[str, float] | None = None
    indicadores: list[str] | None = None
    data_fim: date | None = None
    observacoes: str | None = None

class PoliticaJuventudeStatusUpdate(BaseModel):
    status: StatusPoliticaJuventude

class PoliticaJuventudeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_politica: str
    nome: str
    descricao: str
    area_interesse: AreaInteresse
    data_inicio: date
    data_fim: date | None = None
    status: StatusPoliticaJuventude
    metas: dict[str, float] | None = None
    indicadores: list[str] | None = None
    data_cadastro: date
    observacoes: str | None = None
    ativa: bool