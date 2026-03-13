from __future__ import annotations
from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.governance.statistics.domain.enums import TipoDashboard

class DashboardCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=200)
    descricao: str | None = Field(None, max_length=1000)
    tipo: TipoDashboard = TipoDashboard.OPERACIONAL
    configuracoes: dict[str, Any] | None = None
    kpi_ids: list[int] = Field(default_factory=list)

class DashboardUpdate(BaseModel):
    nome: str | None = Field(None, min_length=3, max_length=200)
    descricao: str | None = Field(None, max_length=1000)
    tipo: TipoDashboard | None = None
    configuracoes: dict[str, Any] | None = None
    kpi_ids: list[int] | None = None

class DashboardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    descricao: str | None
    tipo: TipoDashboard
    configuracoes: dict[str, Any] | None
    kpi_ids: list[int]
    criado_por: int | None
    data_criacao: datetime
    data_atualizacao: datetime

class DashboardListaResponse(BaseModel):
    dashboards: list[DashboardResponse]
    total: int