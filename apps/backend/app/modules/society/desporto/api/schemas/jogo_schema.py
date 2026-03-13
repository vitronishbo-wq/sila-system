from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.modules.society.desporto.domain.enums import StatusJogo

class JogoCreate(BaseModel):
    competicao_id: UUID
    clube_casa_id: UUID
    clube_fora_id: UUID
    data_jogo: date
    local: str = Field(..., min_length=3)
    municipio: str
    provincia: str
    codigo_obra_instalacao: str | None = None
    atracao_turistica_id: UUID | None = None
    publico_estimado: int | None = Field(default=None, ge=0)
    observacoes: str | None = None

class JogoUpdate(BaseModel):
    data_jogo: date | None = None
    local: str | None = Field(default=None, min_length=3)
    municipio: str | None = None
    provincia: str | None = None
    status: StatusJogo | None = None
    codigo_obra_instalacao: str | None = None
    atracao_turistica_id: UUID | None = None
    publico_estimado: int | None = Field(default=None, ge=0)
    publico_presente: int | None = Field(default=None, ge=0)
    ativo: bool | None = None
    observacoes: str | None = None

class JogoResultadoUpdate(BaseModel):
    placar_casa: int = Field(..., ge=0)
    placar_fora: int = Field(..., ge=0)

class JogoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_jogo: str
    competicao_id: UUID
    clube_casa_id: UUID
    clube_fora_id: UUID
    data_jogo: date
    local: str
    municipio: str
    provincia: str
    data_cadastro: date
    status: StatusJogo
    placar_casa: int | None = None
    placar_fora: int | None = None
    codigo_obra_instalacao: str | None = None
    atracao_turistica_id: UUID | None = None
    publico_estimado: int | None = None
    publico_presente: int | None = None
    ativo: bool
    observacoes: str | None = None