from __future__ import annotations
from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.public_security.domain.enums import PrioridadeOcorrencia, StatusOcorrencia, TipoOcorrencia

class OcorrenciaCreate(BaseModel):
    unidade_id: UUID
    tipo: TipoOcorrencia
    prioridade: PrioridadeOcorrencia
    data_ocorrencia: datetime
    descricao: str = Field(..., min_length=5)
    municipio: str
    provincia: str
    policial_responsavel_id: UUID | None = None
    endereco: str | None = None
    vitimas: int = Field(default=0, ge=0)
    suspeitos: int = Field(default=0, ge=0)
    preso_em_flagrante: bool = False
    observacoes: str | None = None
    citizen_id: UUID | None = None

class OcorrenciaStatusUpdate(BaseModel):
    status: StatusOcorrencia
    observacoes: str | None = None

class OcorrenciaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_ocorrencia: str
    unidade_id: UUID
    policial_responsavel_id: UUID | None = None
    tipo: TipoOcorrencia
    status: StatusOcorrencia
    prioridade: PrioridadeOcorrencia
    data_ocorrencia: datetime
    data_registro: date
    municipio: str
    provincia: str
    vitimas: int
    suspeitos: int
    preso_em_flagrante: bool
    ativo: bool