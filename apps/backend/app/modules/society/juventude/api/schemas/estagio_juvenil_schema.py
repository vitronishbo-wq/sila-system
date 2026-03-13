from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.modules.society.juventude.domain.enums import AreaInteresse, StatusEstagio

class EstagioJuvenilCreate(BaseModel):
    jovem_id: UUID
    instituicao: str = Field(..., min_length=3)
    area_interesse: AreaInteresse
    cargo: str = Field(..., min_length=2)
    carga_horaria_semanal: int = Field(..., gt=0)
    data_inicio: date
    bolsa_auxilio: Decimal | None = None
    data_fim: date | None = None
    observacoes: str | None = None

class EstagioJuvenilStatusUpdate(BaseModel):
    status: StatusEstagio

class EstagioJuvenilResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_estagio: str
    jovem_id: UUID
    instituicao: str
    area_interesse: AreaInteresse
    cargo: str
    carga_horaria_semanal: int
    data_inicio: date
    data_fim: date | None = None
    status: StatusEstagio
    bolsa_auxilio: Decimal | None = None
    data_cadastro: date
    observacoes: str | None = None
    ativo: bool