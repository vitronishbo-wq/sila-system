from __future__ import annotations
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.resources.pescas.domain.enums import TipoEmbarcacao

class EmbarcacaoCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    tipo: TipoEmbarcacao
    comprimento: Decimal
    arqueacao_bruta: Decimal
    porto_registro: str
    proprietario_id: UUID

class EmbarcacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    nome: str
    numero_inscricao: str
    tipo: TipoEmbarcacao
    comprimento: Decimal
    arqueacao_bruta: Decimal
    porto_registro: str
    proprietario_id: UUID
    armador_id: Optional[UUID] = None
    licenca_id: Optional[UUID] = None