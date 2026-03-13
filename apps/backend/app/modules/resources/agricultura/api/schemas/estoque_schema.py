from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusEstoque

class EstoqueCreate(BaseModel):
    codigo_insumo: str
    quantidade_minima: float

class EstoqueResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_estoque: str
    codigo_insumo: str
    quantidade_atual: float
    quantidade_minima: float
    status: StatusEstoque
    data_atualizacao: datetime