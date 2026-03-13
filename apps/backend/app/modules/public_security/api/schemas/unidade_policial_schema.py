from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.public_security.domain.enums import StatusUnidadePolicial, TipoUnidadePolicial

class UnidadePolicialCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    tipo: TipoUnidadePolicial
    municipio: str
    provincia: str
    endereco: str
    comandante: str
    telefone: str | None = None
    email: str | None = None
    observacoes: str | None = None

class UnidadePolicialStatusUpdate(BaseModel):
    status: StatusUnidadePolicial
    motivo: str | None = None

class UnidadePolicialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_unidade: str
    nome: str
    tipo: TipoUnidadePolicial
    municipio: str
    provincia: str
    comandante: str
    data_ativacao: date
    status: StatusUnidadePolicial
    ativo: bool