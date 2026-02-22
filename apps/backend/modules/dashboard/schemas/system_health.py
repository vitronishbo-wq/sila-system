"""
Schemas para saúde do sistema - SILA System
Fase 1: Módulos Críticos
"""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class SystemHealthBase(BaseModel):
    """Schema base para saúde do sistema"""

    service_name: str = Field(..., description="Nome do serviço")
    service_type: str = Field(
        ..., description="Tipo do serviço (api, database, cache, etc.)"
    )
    status: str = Field(..., description="Status: healthy, warning, critical, down")
    is_active: bool = Field(default=True, description="Se o serviço está ativo")

    # Métricas de performance
    response_time: Optional[float] = Field(
        default=None, description="Tempo de resposta em ms"
    )
    cpu_usage: Optional[float] = Field(default=None, description="Uso de CPU em %")
    memory_usage: Optional[float] = Field(
        default=None, description="Uso de memória em %"
    )
    disk_usage: Optional[float] = Field(default=None, description="Uso de disco em %")

    # Informações de conexão
    endpoint: Optional[str] = Field(default=None, description="Endpoint do serviço")
    port: Optional[int] = Field(default=None, description="Porta do serviço")

    # Detalhes de erro
    last_error: Optional[datetime] = Field(
        default=None, description="Último erro registrado"
    )
    error_message: Optional[str] = Field(default=None, description="Mensagem de erro")

    # Configurações
    config: Optional[Dict[str, Any]] = Field(
        default=None, description="Configurações específicas"
    )


class SystemHealthCreate(SystemHealthBase):
    """Schema para criação de monitoramento de saúde"""


class SystemHealthUpdate(BaseModel):
    """Schema para atualização de saúde do sistema"""

    status: Optional[str] = None
    is_active: Optional[bool] = None
    response_time: Optional[float] = None
    cpu_usage: Optional[float] = None
    memory_usage: Optional[float] = None
    disk_usage: Optional[float] = None
    endpoint: Optional[str] = None
    port: Optional[int] = None
    last_error: Optional[datetime] = None
    error_message: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


class SystemHealthResponse(SystemHealthBase):
    """Schema para resposta de saúde do sistema"""

    id: int
    last_check: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SystemHealthSummary(BaseModel):
    """Schema resumido para status geral do sistema"""

    overall_status: str = Field(description="Status geral: healthy, warning, critical")
    healthy_services: int = Field(description="Número de serviços saudáveis")
    total_services: int = Field(description="Total de serviços monitorados")
    last_check: datetime = Field(description="Última verificação geral")
    services: list[SystemHealthResponse] = Field(description="Lista de serviços")

    model_config = ConfigDict(from_attributes=True)
