"""Service Registry Schemas - Pydantic validation models"""

from pydantic import BaseModel, ConfigDict
from typing import Optional


class ServiceRegistryBase(BaseModel):
    """Base schema for ServiceRegistry"""

    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ServiceRegistryCreate(ServiceRegistryBase):
    """Schema for creating ServiceRegistry"""

    pass


class ServiceRegistryUpdate(BaseModel):
    """Schema for updating ServiceRegistry"""

    name: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ServiceRegistryRead(ServiceRegistryBase):
    """Schema for reading ServiceRegistry"""

    id: int

    model_config = ConfigDict(from_attributes=True)


# Deprecated — Mantidos apenas por compatibilidade retroativa
class ServiceForwardRequest(BaseModel):
    """Request schema for service forward (deprecated)"""

    pass


class ServiceForwardResponse(BaseModel):
    """Response schema for service forward (deprecated)"""

    pass


class ServiceOut(BaseModel):
    """Output schema for service (deprecated)"""

    pass
