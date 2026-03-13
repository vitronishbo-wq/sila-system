from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.resources.agricultura.domain.enums import TipoInsumo

class InsumoCreate(BaseModel):
    nome: str
    tipo: TipoInsumo
    unidade_medida: str
    quantidade_inicial: float
    custo_unitario: float

class MovimentoInsumoInput(BaseModel):
    quantidade: float

class InsumoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_insumo: str
    nome: str
    tipo: TipoInsumo
    unidade_medida: str
    quantidade_estoque: float
    custo_unitario: float
    data_registro: date
    ativo: bool