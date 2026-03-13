from __future__ import annotations
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class FiscalizacaoCreate(BaseModel):
    embarcacao_id: UUID
    local: str
    agente: str
    regular: bool
    observacoes: Optional[str] = None

class FiscalizacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    embarcacao_id: UUID
    data_fiscalizacao: datetime
    local: str
    agente: str
    regular: bool
    observacoes: Optional[str] = None