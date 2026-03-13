from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.society.juventude.domain.enums import AreaInteresse, StatusEmpreendimento

class EmpreendedorismoJuvenilCreate(BaseModel):
    jovem_id: UUID
    nome_negocio: str = Field(..., min_length=3)
    area_interesse: AreaInteresse
    receita_mensal: Decimal | None = None
    valor_credito: Decimal | None = None
    observacoes: str | None = None

class EmpreendedorismoJuvenilStatusUpdate(BaseModel):
    status: StatusEmpreendimento

class EmpreendedorismoJuvenilResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_empreendimento: str
    jovem_id: UUID
    nome_negocio: str
    area_interesse: AreaInteresse
    status: StatusEmpreendimento
    receita_mensal: Decimal | None = None
    valor_credito: Decimal | None = None
    data_cadastro: date
    observacoes: str | None = None
    ativo: bool