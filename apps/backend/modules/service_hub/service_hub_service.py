from .crud import CRUDService, get_service_crud
from sqlalchemy.ext.asyncio import AsyncSession


class ServiceHubService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.crud = get_service_crud()

    async def list_services(self, skip: int = 0, limit: int = 100):
        return await self.crud.get_multi(self.db, skip=skip, limit=limit)

    async def create_service(self, service_in):
        return await self.crud.create(self.db, obj_in=service_in)

    async def update_service(self, service_id: int, service_in):
        db_obj = await self.crud.get(self.db, service_id)
        if not db_obj:
            return None
        return await self.crud.update(self.db, db_obj=db_obj, obj_in=service_in)
