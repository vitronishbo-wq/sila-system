from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from modules.service_hub.schemas.service_hub_crud import (
    ServiceRegistryCreate,
    ServiceRegistryInDB,
)
from modules.service_hub.services.service_hub_service import ServiceHubService
from modules.database import get_db

router = APIRouter()


@router.post("/service_hub/register", response_model=ServiceRegistryInDB)
async def register_service(
    service: ServiceRegistryCreate, db: AsyncSession = Depends(get_db)
):
    svc = ServiceHubService(db)
    try:
        return await svc.register_service(service, user_id=1)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/service_hub/{service_id}", response_model=ServiceRegistryInDB)
async def get_service(service_id: int, db: AsyncSession = Depends(get_db)):
    svc = ServiceHubService(db)
    service_obj = await svc.get_service(service_id)
    if not service_obj:
        raise HTTPException(status_code=404, detail="Service not found")
    return service_obj
