"""
Schemas para estatísticas do dashboard - SILA System
Fase 1: Módulos Críticos
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DashboardStatsBase(BaseModel):
    """Schema base para estatísticas do dashboard"""

    # Estatísticas de usuários
    total_users: int = Field(default=0, description="Total de usuários no sistema")
    active_users: int = Field(default=0, description="Usuários ativos")
    new_users_today: int = Field(default=0, description="Novos usuários hoje")

    # Estatísticas de serviços
    total_services: int = Field(default=0, description="Total de serviços")
    active_services: int = Field(default=0, description="Serviços ativos")
    services_usage_count: int = Field(
        default=0, description="Contagem de uso dos serviços"
    )

    # Estatísticas de requisições
    total_requests: int = Field(default=0, description="Total de requisições")
    pending_requests: int = Field(default=0, description="Requisições pendentes")
    completed_requests: int = Field(default=0, description="Requisições concluídas")
    rejected_requests: int = Field(default=0, description="Requisições rejeitadas")

    # Métricas de performance
    avg_response_time: float = Field(
        default=0.0, description="Tempo médio de resposta em ms"
    )
    system_uptime: float = Field(
        default=0.0, description="Tempo de funcionamento do sistema"
    )

    # Status do sistema
    system_health_status: str = Field(
        default="healthy", description="Status de saúde do sistema"
    )
    last_error_time: Optional[datetime] = Field(
        default=None, description="Último erro registrado"
    )


class DashboardStatsCreate(DashboardStatsBase):
    """Schema para criação de estatísticas"""


class DashboardStatsUpdate(BaseModel):
    """Schema para atualização de estatísticas"""

    total_users: Optional[int] = None
    active_users: Optional[int] = None
    new_users_today: Optional[int] = None
    total_services: Optional[int] = None
    active_services: Optional[int] = None
    services_usage_count: Optional[int] = None
    total_requests: Optional[int] = None
    pending_requests: Optional[int] = None
    completed_requests: Optional[int] = None
    rejected_requests: Optional[int] = None
    avg_response_time: Optional[float] = None
    system_uptime: Optional[float] = None
    system_health_status: Optional[str] = None
    last_error_time: Optional[datetime] = None


class DashboardStatsResponse(DashboardStatsBase):
    """Schema para resposta de estatísticas"""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DashboardStatsSummary(BaseModel):
    """Schema resumido para resposta rápida"""

    total_users: int
    total_services: int
    active_requests: int
    completed_requests: int
    system_health: str
    last_updated: datetime

    model_config = ConfigDict(from_attributes=True)
