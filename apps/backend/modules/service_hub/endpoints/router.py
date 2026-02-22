# modules/service_hub/endpoints/router.py
from datetime import datetime
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from core.db.session import get_async_db
from modules.service_hub.crud import get_service_registry_crud
from modules.models import ServiceStatus
from modules.service_hub.schemas.service_hub_crud import (
    ServiceRegistryCreate,
    ServiceRegistryInDB,
    ServiceRegistryUpdate,
)

router = APIRouter(prefix="/service-hub", tags=["service-hub"])


@router.post("/services", status_code=status.HTTP_201_CREATED, response_model=ServiceRegistryInDB)
async def create_service(
    service_in: ServiceRegistryCreate,
    db: AsyncSession = Depends(get_async_db),
):
    """Regista novo serviço no hub."""
    crud = get_service_registry_crud()
    existing = await crud.get_by_name(db, service_in.name)
    if existing:
        raise HTTPException(status_code=400, detail="Serviço já existe")

    service_in.status = ServiceStatus.ACTIVE
    service_in.last_health_check = datetime.utcnow()
    return await crud.create(db, obj_in=service_in)


@router.get("/services", response_model=List[ServiceRegistryInDB])
async def list_services(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
):
    """Lista serviços registados com paginação."""
    crud = get_service_registry_crud()
    return await crud.get_multi(db, skip=skip, limit=limit)


@router.get("/services/{service_id}", response_model=ServiceRegistryInDB)
async def get_service(service_id: int, db: AsyncSession = Depends(get_async_db)):
    """Retorna detalhes de serviço específico."""
    crud = get_service_registry_crud()
    service = await crud.get(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return service


@router.put("/services/{service_id}", response_model=ServiceRegistryInDB)
async def update_service(
    service_id: int,
    service_in: ServiceRegistryUpdate,
    db: AsyncSession = Depends(get_async_db),
):
    """Atualiza dados de serviço existente."""
    crud = get_service_registry_crud()
    service = await crud.get(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return await crud.update(db, db_obj=service, obj_in=service_in)


@router.delete("/services/{service_id}", status_code=204)
async def delete_service(service_id: int, db: AsyncSession = Depends(get_async_db)):
    """Remove serviço do registo."""
    crud = get_service_registry_crud()
    service = await crud.get(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    await crud.remove(db, service_id)


@router.post("/services/{service_id}/activate", response_model=ServiceRegistryInDB)
async def activate_service(service_id: int, db: AsyncSession = Depends(get_async_db)):
    """Ativa serviço registado."""
    crud = get_service_registry_crud()
    service = await crud.get(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    service.status = ServiceStatus.ACTIVE
    service.last_health_check = datetime.utcnow()
    return await crud.update(db, db_obj=service, obj_in=ServiceRegistryUpdate())


@router.post("/services/{service_id}/deactivate", response_model=ServiceRegistryInDB)
async def deactivate_service(service_id: int, db: AsyncSession = Depends(get_async_db)):
    """Desativa serviço registado."""
    crud = get_service_registry_crud()
    service = await crud.get(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    service.status = ServiceStatus.INACTIVE
    return await crud.update(db, db_obj=service, obj_in=ServiceRegistryUpdate())


@router.post("/services/{service_id}/forward", response_model=Dict)
async def forward_request(
    service_id: int,
    payload: Dict,
    db: AsyncSession = Depends(get_async_db),
):
    """Encaminha payload para endpoint do serviço registado."""
    crud = get_service_registry_crud()
    service = await crud.get(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(service.endpoint, json=payload, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Falha ao encaminhar: {str(e)}")