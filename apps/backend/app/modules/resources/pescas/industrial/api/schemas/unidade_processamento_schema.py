from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.resources.pescas.industrial.domain.enums import ClassificacaoIndustrial, TipoProcessamento

class UnidadeProcessamentoCreate(BaseModel):
    cnpj: str = Field(..., pattern='^\\d{2}\\.\\d{3}\\.\\d{3}/\\d{4}-\\d{2}$')
    razao_social: str = Field(..., min_length=3)
    tipo_processamento: list[TipoProcessamento]
    classificacao: ClassificacaoIndustrial
    capacidade_kg_dia: Decimal = Field(..., gt=0)
    area_total_m2: Decimal = Field(..., gt=0)
    area_producao_m2: Decimal = Field(..., gt=0)
    area_armazenagem_m2: Decimal = Field(..., gt=0)
    numero_funcionarios: int = Field(..., ge=1)
    endereco: str
    municipio: str
    provincia: str
    armador_id: UUID | None = None
    responsavel_tecnico_id: UUID | None = None

class UnidadeProcessamentoUpdateCapacidade(BaseModel):
    capacidade_kg_dia: Decimal = Field(..., gt=0)

class UnidadeProcessamentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    cnpj: str
    razao_social: str
    tipo_processamento: list[TipoProcessamento]
    classificacao: ClassificacaoIndustrial
    capacidade_kg_dia: Decimal
    area_total_m2: Decimal
    area_producao_m2: Decimal
    area_armazenagem_m2: Decimal
    numero_funcionarios: int
    endereco: str
    municipio: str
    provincia: str
    armador_id: UUID | None = None
    data_inauguracao: date