from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ResumoOperacionalFlorestal(BaseModel):
    total_operadores: int = Field(ge=0)
    total_unidades_manejo: int = Field(ge=0)
    total_planos_manejo: int = Field(ge=0)
    total_inventarios: int = Field(ge=0)
    media_unidades_por_operador: float = Field(ge=0.0)
    media_planos_por_unidade: float = Field(ge=0.0)


class IntegracaoModuloFlorestal(BaseModel):
    modulo: str
    available: bool
    detalhes: dict[str, Any] = Field(default_factory=dict)


class IntegracaoTransversalFlorestal(BaseModel):
    integracao_ok: bool
    modulos_ativos: int = Field(ge=0)
    modulos_totais: int = Field(ge=0)
    modulos: list[IntegracaoModuloFlorestal] = Field(default_factory=list)


class DashboardEstatisticoFlorestal(BaseModel):
    operacional: ResumoOperacionalFlorestal
    integracao: IntegracaoTransversalFlorestal


class EstatisticaFlorestalCreate(BaseModel):
    placeholder: bool = True


class EstatisticaFlorestalResponse(DashboardEstatisticoFlorestal):
    pass
