"""
Schemas Pydantic para o módulo de Cidadania (Ajustado para IDs Inteiros).
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict

class ServiceCategory(str, Enum):
    DOCUMENTOS = "documentos"
    CERTIDOES = "certidoes"
    REGISTROS = "registros"
    AUTORIZACOES = "autorizacoes"
    LICENCAS = "licencas"
    OUTROS = "outros"

class ServiceStatus(str, Enum):
    PENDING = "pending"
    IN_REVIEW = "in_review"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REJECTED = "rejected"

class PriorityLevel(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

# --- Schemas de Serviço ---

class CitizenshipServiceBase(BaseModel):
    name: str = Field(..., description="Nome do serviço")
    description: str = Field(..., description="Descrição detalhada do serviço")
    category: ServiceCategory = Field(..., description="Categoria do serviço")
    estimated_days: int = Field(..., ge=1, le=365)
    requirements: List[str] = Field(default_factory=list)
    is_active: bool = Field(True)

class CitizenshipServiceRead(CitizenshipServiceBase):
    id: int # Alterado de UUID para int para alinhar com o DB
    code: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Schemas de Solicitação (Requests) ---

class ServiceRequestBase(BaseModel):
    service_code: str
    priority: PriorityLevel = PriorityLevel.NORMAL
    observations: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None

class ServiceRequestCreate(ServiceRequestBase):
    pass

class ServiceRequestRead(ServiceRequestBase):
    id: int # Alterado para int
    user_id: int # Usamos user_id em vez de citizen_id para alinhar com o modelo User
    status: ServiceStatus
    protocol_number: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    # Dados denormalizados para o Frontend
    service_name: str
    service_category: ServiceCategory
    user_full_name: str # Nome vindo do modelo User
    
    model_config = ConfigDict(from_attributes=True)

class ServiceRequestStatus(BaseModel):
    id: int
    status: ServiceStatus
    protocol_number: str
    service_name: str
    progress_percentage: Optional[int] = Field(None, ge=0, le=100)
    model_config = ConfigDict(from_attributes=True)