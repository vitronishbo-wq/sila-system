from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from apps.backend.app.modules.governance.statistics.domain.enums import StatusKPI


class KPICreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=200)
    descricao: str = Field(..., min_length=3, max_length=2000)
    metrica_id: int = Field(..., gt=0)
    valor_alvo: float | None = Field(None, ge=0)
    unidade: str = Field(..., max_length=50)
    peso: float = Field(1.0, ge=0, le=10)
    limite_inferior: float | None = None
    limite_superior: float | None = None

    @model_validator(mode="after")
    def validar_limites(self) -> KPICreate:
        if (
            self.limite_inferior is not None
            and self.limite_superior is not None
            and (self.limite_inferior > self.limite_superior)
        ):
            raise ValueError("limite_inferior nao pode ser maior que limite_superior")
        return self


class KPIUpdate(BaseModel):
    nome: str | None = Field(None, min_length=3, max_length=200)
    descricao: str | None = Field(None, min_length=3, max_length=2000)
    valor_alvo: float | None = Field(None, ge=0)
    valor_atual: float | None = None
    status: StatusKPI | None = None
    peso: float | None = Field(None, ge=0, le=10)
    limite_inferior: float | None = None
    limite_superior: float | None = None


class KPIValorUpdate(BaseModel):
    valor: float


class KPIResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    descricao: str
    metrica_id: int
    valor_alvo: float | None
    valor_atual: float | None
    unidade: str
    status: StatusKPI
    peso: float
    limite_inferior: float | None
    limite_superior: float | None
    performance: float
    status_cor: str
    data_criacao: datetime
    data_atualizacao: datetime


class KPIListaResponse(BaseModel):
    kpis: list[KPIResponse]
    total: int
    pagina: int
    tamanho_pagina: int
    filtros_aplicados: dict
