"""Service Hub Schemas - Pydantic validation models"""

from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class ServiceLocationBase(BaseModel):
    """Base schema for ServiceLocation"""

    province: str
    address: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ServiceLocationCreate(ServiceLocationBase):
    """Schema for creating ServiceLocation"""

    service_id: int


class ServiceLocationUpdate(BaseModel):
    """Schema for updating ServiceLocation"""

    province: Optional[str] = None
    address: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ServiceLocationRead(ServiceLocationBase):
    """Schema for reading ServiceLocation"""

    id: int
    service_id: int

    model_config = ConfigDict(from_attributes=True)


class ServiceBase(BaseModel):
    """Base schema for Service"""

    name: str
    status: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ServiceCreate(ServiceBase):
    """Schema for creating Service"""

    pass


class ServiceUpdate(BaseModel):
    """Schema for updating Service"""

    name: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ServiceRead(ServiceBase):
    """Schema for reading Service"""

    id: int

    model_config = ConfigDict(from_attributes=True)


class ServiceWithLocations(ServiceRead):
    """Schema for reading Service with its locations"""

    locations: List[ServiceLocationRead] = []

    model_config = ConfigDict(from_attributes=True)


class ServiceFilters(BaseModel):
    """Filter schema for services (deprecated)"""

    name: Optional[str] = None
    status: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ServiceLocationFilters(BaseModel):
    """Filter schema for service locations (deprecated)"""

    province: Optional[str] = None
    service_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
