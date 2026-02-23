from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime


class ServiceRequestCreate(BaseModel):
    """Schema para criação de pedido"""
    service_type: str = Field(..., description="Tipo de serviço")
    title: str = Field(..., min_length=5, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    channel: str = Field("WEB", description="Canal de origem")
    priority: str = Field("MEDIA", description="Prioridade")
    metadata: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    
    @field_validator('service_type')
    @classmethod
    def validate_service_type(cls, v):
        from ...domain.enums import ServiceType
        if v not in [st.value for st in ServiceType]:
            raise ValueError(f"Tipo de serviço inválido: {v}")
        return v


class ServiceRequestResponse(BaseModel):
    """Schema para resposta de pedido"""
    id: UUID
    request_number: Optional[str]
    citizen_id: UUID
    created_by_user_id: UUID
    assigned_to_user_id: Optional[UUID]
    service_type: str
    title: str
    description: Optional[str]
    status: str
    priority: str
    channel: str
    workflow_instance_id: Optional[UUID]
    tags: List[str]
    created_at: datetime
    updated_at: Optional[datetime]
    submitted_at: Optional[datetime]
    completed_at: Optional[datetime]
    deadline: Optional[datetime]
    is_active: bool
    is_draft: bool
    is_terminal: bool
    
    model_config = ConfigDict(from_attributes=True)


class ServiceRequestDetailResponse(ServiceRequestResponse):
    """Schema detalhado com metadados"""
    metadata: Dict[str, Any]
    workflow_data: Dict[str, Any]
    sla_due_at: Optional[datetime]
    sla_breached: bool


class ServiceRequestListResponse(BaseModel):
    """Schema para listagem de pedidos"""
    total: int
    items: List[ServiceRequestResponse]


class ServiceRequestStatusUpdate(BaseModel):
    """Schema para atualização de status"""
    status: str = Field(..., description="Novo status")
    reason: Optional[str] = Field(None, description="Motivo da mudança")
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        from ...domain.enums import ServiceRequestStatus
        if v not in [s.value for s in ServiceRequestStatus]:
            raise ValueError(f"Status inválido: {v}")
        return v


class ServiceRequestAssign(BaseModel):
    """Schema para atribuição de pedido"""
    assigned_to_user_id: UUID = Field(..., description="ID do operador")


class ServiceRequestSearch(BaseModel):
    """Schema para pesquisa de pedidos"""
    query: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    service_type: Optional[str] = None
    citizen_id: Optional[UUID] = None
    assigned_to: Optional[UUID] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    skip: int = 0
    limit: int = 100


class ServiceRequestStatsResponse(BaseModel):
    """Schema para estatísticas"""
    by_status: Dict[str, int]
    total: int
