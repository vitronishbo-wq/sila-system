from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from modules.service_hub.models import ServiceStatus


class ServiceRegistryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[ServiceStatus] = ServiceStatus.INACTIVE
    last_health_check: Optional[datetime] = None


class ServiceRegistryInDB(ServiceRegistryCreate):
    id: int

    class Config:
        orm_mode = True
