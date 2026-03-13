from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.resources.agricultura.domain.enums import StatusEquipamento, TipoEquipamento

class EquipamentoCreate(BaseModel):
    nome: str
    tipo: TipoEquipamento
    fabricante: str | None = None
    modelo: str | None = None
    ano_fabricacao: int | None = None
    data_aquisicao: date | None = None

class UsoEquipamentoInput(BaseModel):
    horas: float

class EquipamentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_equipamento: str
    nome: str
    tipo: TipoEquipamento
    fabricante: str | None
    modelo: str | None
    ano_fabricacao: int | None
    data_aquisicao: date | None
    status: StatusEquipamento
    horas_uso: float
    ultima_manutencao: date | None = None