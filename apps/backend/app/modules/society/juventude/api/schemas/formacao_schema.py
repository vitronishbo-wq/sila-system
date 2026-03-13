from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.modules.society.juventude.domain.enums import StatusFormacao

class FormacaoCreate(BaseModel):
    jovem_id: UUID
    programa_id: UUID | None = None
    nome_curso: str = Field(..., min_length=3)
    instituicao: str = Field(..., min_length=3)
    carga_horaria: int = Field(..., gt=0)
    data_inicio: date
    data_fim: date | None = None
    observacoes: str | None = None

class FormacaoStatusUpdate(BaseModel):
    status: StatusFormacao
    certificado_emitido: bool | None = None

class FormacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_formacao: str
    jovem_id: UUID
    programa_id: UUID | None = None
    nome_curso: str
    instituicao: str
    carga_horaria: int
    data_inicio: date
    data_fim: date | None = None
    certificado_emitido: bool
    status: StatusFormacao
    data_cadastro: date
    observacoes: str | None = None
    ativo: bool