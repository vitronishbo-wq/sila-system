from datetime import datetime
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from modules.service_hub.crud import get_service_registry_crud
from modules.service_hub.schemas.service_hub_crud import (
    ServiceRegistryCreate,
    ServiceRegistryInDB,
)
from modules.service_hub.models import ServiceStatus


class ServiceHubService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.crud = get_service_registry_crud()

    async def register_service(
        self, service_data: ServiceRegistryCreate, user_id: int
    ) -> ServiceRegistryInDB:
        existing_service = await self.crud.get_by_name(self.db, service_data.name)
        if existing_service:
            raise ValueError(f"Service with name {service_data.name} already exists")
        service_data.status = ServiceStatus.ACTIVE
        service_data.last_health_check = datetime.now()
        return await self.crud.create(self.db, service_data)

    async def get_service(self, service_id: int) -> Optional[ServiceRegistryInDB]:
        return await self.crud.get(self.db, service_id)

    async def get_services(
        self, skip: int = 0, limit: int = 100
    ) -> List[ServiceRegistryInDB]:
        return await self.crud.get_multi(self.db, skip=skip, limit=limit)
