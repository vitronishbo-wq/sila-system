"""
Schemas para log de atividades - SILA System
Fase 1: Módulos Críticos
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ActivityLogBase(BaseModel):
    """Schema base para log de atividades"""

    action: str = Field(..., description="Ação realizada")
    resource_type: str = Field(..., description="Tipo do recurso afetado")
    resource_id: Optional[str] = Field(default=None, description="ID do recurso")

    # Informações do usuário
    user_id: Optional[int] = Field(default=None, description="ID do usuário")
    user_email: Optional[str] = Field(default=None, description="Email do usuário")
    user_role: Optional[str] = Field(default=None, description="Role do usuário")

    # Detalhes da atividade
    description: Optional[str] = Field(
        default=None, description="Descrição da atividade"
    )
    ip_address: Optional[str] = Field(default=None, description="Endereço IP")
    user_agent: Optional[str] = Field(default=None, description="User Agent")

    # Resultado
    status: str = Field(
        default="success", description="Status: success, error, warning"
    )
    status_code: Optional[int] = Field(
        default=None, description="Código de status HTTP"
    )
    error_message: Optional[str] = Field(default=None, description="Mensagem de erro")

    # Dados de auditoria
    old_values: Optional[Dict[str, Any]] = Field(
        default=None, description="Valores anteriores"
    )
    new_values: Optional[Dict[str, Any]] = Field(
        default=None, description="Novos valores"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Metadados adicionais"
    )


class ActivityLogCreate(ActivityLogBase):
    """Schema para criação de log de atividade"""


class ActivityLogUpdate(BaseModel):
    """Schema para atualização de log de atividade"""

    description: Optional[str] = None
    status: Optional[str] = None
    status_code: Optional[int] = None
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ActivityLogResponse(ActivityLogBase):
    """Schema para resposta de log de atividade"""

    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class ActivityLogListResponse(BaseModel):
    """Schema para lista de logs de atividades"""

    items: List[ActivityLogResponse]
    total: int
    page: int
    limit: int
    total_pages: int

    model_config = ConfigDict(from_attributes=True)


class ActivityLogFilters(BaseModel):
    """Schema para filtros de busca de atividades"""

    action: Optional[str] = None
    resource_type: Optional[str] = None
    user_id: Optional[int] = None
    user_email: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)
