from __future__ import annotations
from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.resources.florestas.domain.enums import TipoOperadorFlorestal

class OperadorFlorestalCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    nif: str = Field(..., min_length=5)
    tipo_operador: TipoOperadorFlorestal = TipoOperadorFlorestal.EMPRESA

class OperadorFlorestalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    nome: str
    nif: str
    tipo_operador: TipoOperadorFlorestal
    data_registro: date
    ativo: bool
    observacoes: Optional[str] = None