"""Service Hub CRUD Schemas - Pydantic V2 Models"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# =============================================================================
# SERVICE SCHEMAS
# =============================================================================


class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(ServiceBase):
    pass


class ServiceInDB(ServiceBase):
    id: int
    status: str

    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# SERVICE LOCATION SCHEMAS
# =============================================================================


class ServiceLocationBase(BaseModel):
    service_id: int
    province: str
    address: Optional[str] = None


class ServiceLocationCreate(ServiceLocationBase):
    pass


class ServiceLocationUpdate(ServiceLocationBase):
    pass


class ServiceLocationInDB(ServiceLocationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# SERVICE REGISTRY SCHEMAS
# =============================================================================


class ServiceRegistryBase(BaseModel):
    name: str
    endpoint: str
    is_public: Optional[bool] = True


class ServiceRegistryCreate(ServiceRegistryBase):
    pass


class ServiceRegistryUpdate(ServiceRegistryBase):
    status: Optional[str] = None
    last_health_check: Optional[datetime] = None


class ServiceRegistryInDB(ServiceRegistryBase):
    id: int
    status: str
    last_health_check: datetime

    model_config = ConfigDict(from_attributes=True)
