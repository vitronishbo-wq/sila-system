from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.public_security.domain.enums import StatusEvidencia, TipoEvidencia

class EvidenciaCreate(BaseModel):
    vestigio_id: UUID
    tipo: TipoEvidencia
    descricao: str = Field(..., min_length=5)
    fonte: str = Field(..., min_length=3)
    confiabilidade: int = Field(default=3, ge=1, le=5)
    analisado_por_id: UUID | None = None
    observacoes: str | None = None
    citizen_id: UUID | None = None

class EvidenciaStatusUpdate(BaseModel):
    status: StatusEvidencia
    observacoes: str | None = None

class EvidenciaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_evidencia: str
    vestigio_id: UUID
    cadeia_custodia_id: UUID
    tipo: TipoEvidencia
    descricao: str
    fonte: str
    confiabilidade: int
    status: StatusEvidencia
    data_registro: date
    analisado_por_id: UUID | None = None
    ativo: bool