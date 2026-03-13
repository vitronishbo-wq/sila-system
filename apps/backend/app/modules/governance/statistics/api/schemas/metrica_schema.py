from __future__ import annotations
from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.governance.statistics.domain.enums import FonteDados, Periodicidade, TipoMetrica

class MetricaCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=200)
    descricao: str = Field(..., min_length=3, max_length=1000)
    tipo: TipoMetrica
    unidade: str = Field(..., max_length=50)
    fonte_dados: FonteDados
    periodicidade: Periodicidade
    formula: str | None = Field(None, max_length=500)
    parametros: dict[str, Any] | None = None

class MetricaUpdate(BaseModel):
    nome: str | None = Field(None, min_length=3, max_length=200)
    descricao: str | None = Field(None, min_length=3, max_length=1000)
    tipo: TipoMetrica | None = None
    unidade: str | None = Field(None, max_length=50)
    fonte_dados: FonteDados | None = None
    periodicidade: Periodicidade | None = None
    formula: str | None = Field(None, max_length=500)
    parametros: dict[str, Any] | None = None
    ativo: bool | None = None

class MetricaValorUpdate(BaseModel):
    valor: float

class MetricaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    descricao: str
    tipo: TipoMetrica
    unidade: str
    fonte_dados: FonteDados
    periodicidade: Periodicidade
    formula: str | None
    parametros: dict[str, Any] | None
    valor_atual: float | None
    valor_anterior: float | None
    variacao_percentual: float | None
    tendencia: str
    ativo: bool
    data_criacao: datetime
    data_atualizacao: datetime
    ultima_atualizacao: datetime | None

class MetricaListaResponse(BaseModel):
    metricas: list[MetricaResponse]
    total: int
    pagina: int
    tamanho_pagina: int
    filtros_aplicados: dict