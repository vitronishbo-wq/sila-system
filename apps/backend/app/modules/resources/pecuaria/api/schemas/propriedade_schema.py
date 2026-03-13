from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class PropriedadeCreate(BaseModel):
    pecuarista_id: UUID
    nome: str
    area_total_ha: float
    municipio: str
    provincia: str

class PropriedadeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_propriedade: str
    pecuarista_id: UUID
    nome: str
    area_total_ha: float
    municipio: str
    provincia: str
    data_cadastro: date
    ativo: bool