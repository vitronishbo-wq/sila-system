from typing import Any, Dict, List, Optional, Type, TypeVar, Generic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Service, ServiceLocation, ServiceRegistry
from .schemas.service_hub_crud import (
    ServiceCreate,
    ServiceUpdate,
    ServiceLocationCreate,
    ServiceLocationUpdate,
    ServiceRegistryCreate,
    ServiceRegistryUpdate,
)

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        result = await db.execute(
            select(self.model).offset(skip).limit(limit).order_by(self.model.id)
        )
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.dict(exclude_unset=True))
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> ModelType:
        result = await db.execute(select(self.model).where(self.model.id == id))
        obj = result.scalar_one()
        await db.delete(obj)
        await db.commit()
        return obj


class CRUDService(CRUDBase[Service, ServiceCreate, ServiceUpdate]):
    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[Service]:
        result = await db.execute(select(Service).where(Service.name == name))
        return result.scalar_one_or_none()


class CRUDServiceLocation(
    CRUDBase[ServiceLocation, ServiceLocationCreate, ServiceLocationUpdate]
):
    async def get_by_service_and_location(
        self, db: AsyncSession, service_id: int, location_id: int
    ) -> Optional[ServiceLocation]:
        result = await db.execute(
            select(ServiceLocation).where(
                (ServiceLocation.service_id == service_id)
                & (ServiceLocation.province == location_id)
            )
        )
        return result.scalar_one_or_none()


class CRUDServiceRegistry(
    CRUDBase[ServiceRegistry, ServiceRegistryCreate, ServiceRegistryUpdate]
):
    async def get_by_name(
        self, db: AsyncSession, name: str
    ) -> Optional[ServiceRegistry]:
        result = await db.execute(
            select(ServiceRegistry).where(ServiceRegistry.name == name)
        )
        return result.scalar_one_or_none()


def get_service_crud() -> CRUDService:
    return CRUDService(Service)


def get_service_location_crud() -> CRUDServiceLocation:
    return CRUDServiceLocation(ServiceLocation)


def get_service_registry_crud() -> CRUDServiceRegistry:
    return CRUDServiceRegistry(ServiceRegistry)
