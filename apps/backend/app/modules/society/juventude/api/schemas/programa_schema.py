from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.society.juventude.domain.enums import StatusPrograma, TipoPrograma

class ProgramaCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    tipo: TipoPrograma
    data_inicio: date
    data_fim: date | None = None
    vagas: int | None = Field(default=None, gt=0)
    municipio: str | None = None
    provincia: str | None = None
    observacoes: str | None = None

class ProgramaStatusUpdate(BaseModel):
    status: StatusPrograma

class ProgramaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_programa: str
    nome: str
    tipo: TipoPrograma
    data_inicio: date
    data_fim: date | None = None
    vagas: int | None = None
    municipio: str | None = None
    provincia: str | None = None
    status: StatusPrograma
    data_cadastro: date
    observacoes: str | None = None
    ativo: bool