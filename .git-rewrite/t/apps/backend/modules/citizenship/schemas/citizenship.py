"""
Schemas Pydantic para o módulo de Cidadania.

Define estruturas de dados para serviços de cidadania, incluindo:
- Catálogo de serviços disponíveis
- Solicitações de serviços
- Controle de status e acompanhamento
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class ServiceCategory(str, Enum):
    """Categorias de serviços de cidadania."""

    DOCUMENTOS = "documentos"
    CERTIDOES = "certidoes"
    REGISTROS = "registros"
    AUTORIZACOES = "autorizacoes"
    LICENCAS = "licencas"
    OUTROS = "outros"


class ServiceStatus(str, Enum):
    """Status possíveis para solicitações de serviço."""

    PENDING = "pending"
    IN_REVIEW = "in_review"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class PriorityLevel(str, Enum):
    """Níveis de prioridade para serviços."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class CitizenshipServiceBase(BaseModel):
    """Schema base para serviços de cidadania."""

    name: str = Field(..., description="Nome do serviço")
    description: str = Field(..., description="Descrição detalhada do serviço")
    category: ServiceCategory = Field(..., description="Categoria do serviço")
    estimated_days: int = Field(..., ge=1, le=365, description="Prazo estimado em dias")
    requirements: List[str] = Field(
        default_factory=list, description="Lista de requisitos"
    )
    is_active: bool = Field(True, description="Se o serviço está ativo")


class CitizenshipServiceCreate(CitizenshipServiceBase):
    """Schema para criação de serviços."""

    priority: PriorityLevel = Field(
        default=PriorityLevel.NORMAL, description="Nível de prioridade"
    )


class CitizenshipServiceRead(CitizenshipServiceBase):
    """Schema para leitura de serviços."""

    id: UUID
    code: str = Field(..., description="Código único do serviço")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CitizenshipServiceList(BaseModel):
    """Schema para lista de serviços."""

    services: List[CitizenshipServiceRead]
    total: int
    categories: List[str]


class ServiceRequestBase(BaseModel):
    """Schema base para solicitações de serviço."""

    service_code: str = Field(..., description="Código do serviço solicitado")
    priority: PriorityLevel = Field(
        default=PriorityLevel.NORMAL, description="Nível de prioridade"
    )
    observations: Optional[str] = Field(None, description="Observações adicionais")
    contact_phone: Optional[str] = Field(None, description="Telefone para contato")
    contact_email: Optional[str] = Field(None, description="Email para contato")


class ServiceRequestCreate(ServiceRequestBase):
    """Schema para criação de solicitações."""


class ServiceRequestUpdate(BaseModel):
    """Schema para atualização de solicitações."""

    observations: Optional[str] = Field(None, description="Observações adicionais")
    contact_phone: Optional[str] = Field(None, description="Telefone para contato")
    contact_email: Optional[str] = Field(None, description="Email para contato")


class ServiceRequestRead(ServiceRequestBase):
    """Schema para leitura de solicitações."""

    id: UUID
    citizen_id: UUID
    status: ServiceStatus
    protocol_number: str = Field(..., description="Número do protocolo")
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    # Dados do serviço solicitado
    service_name: str
    service_category: ServiceCategory
    estimated_completion: Optional[datetime] = None

    # Dados do cidadão (básicos)
    citizen_name: str
    citizen_document: str

    model_config = ConfigDict(from_attributes=True)


class ServiceRequestStatus(BaseModel):
    """Schema para informações de status de solicitação."""

    id: UUID
    status: ServiceStatus
    protocol_number: str
    service_name: str
    created_at: datetime
    estimated_completion: Optional[datetime] = None
    current_step: Optional[str] = None
    progress_percentage: Optional[int] = Field(None, ge=0, le=100)

    model_config = ConfigDict(from_attributes=True)


class ServiceRequestHistory(BaseModel):
    """Schema para histórico de alterações de status."""

    id: UUID
    request_id: UUID
    old_status: Optional[ServiceStatus]
    new_status: ServiceStatus
    changed_by: str
    change_reason: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ServiceRequestFilters(BaseModel):
    """Schema para filtros de busca de solicitações."""

    status: Optional[ServiceStatus] = None
    category: Optional[ServiceCategory] = None
    priority: Optional[PriorityLevel] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None


class ServiceStatistics(BaseModel):
    """Schema para estatísticas de serviços."""

    total_requests: int
    pending_requests: int
    completed_requests: int
    cancelled_requests: int
    avg_processing_time_days: Optional[float]
    services_by_category: Dict[str, int]
    status_distribution: Dict[str, int]


class ServiceRequestSummary(BaseModel):
    """Schema resumido para listagem de solicitações."""

    id: UUID
    protocol_number: str
    service_name: str
    status: ServiceStatus
    priority: PriorityLevel
    created_at: datetime
    citizen_name: str


class ServiceRequestDetail(ServiceRequestRead):
    """Schema detalhado para visualização completa de solicitação."""

    service_description: str
    service_requirements: List[str]
    service_estimated_days: int
    history: List[ServiceRequestHistory] = Field(default_factory=list)


class BulkServiceRequestCreate(BaseModel):
    """Schema para criação de múltiplas solicitações."""

    requests: List[ServiceRequestCreate] = Field(..., min_length=1, max_length=10)


class ServiceRequestSearch(BaseModel):
    """Schema para busca de solicitações."""

    protocol_number: Optional[str] = None
    citizen_document: Optional[str] = None
    citizen_name: Optional[str] = None
    service_name: Optional[str] = None
    status: Optional[ServiceStatus] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    page: int = Field(1, ge=1)
    size: int = Field(20, ge=1, le=100)
