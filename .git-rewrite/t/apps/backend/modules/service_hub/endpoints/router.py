# apps/backend/modules/service_hub/endpoints/router.py
"""Service Hub API Endpoints"""

from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import httpx

from core.db.session import get_async_db
from modules.service_hub.crud import get_service_registry_crud
from modules.service_hub.schemas.service_hub_crud import (
    ServiceRegistryCreate,
    ServiceRegistryInDB,
    ServiceRegistryUpdate,
)
from modules.models import ServiceStatus

# ✅ Corrigido: sem prefixo aqui, será definido no main.py
router = APIRouter(tags=["Service Hub"])

# =============================================================================
# SERVICE REGISTRY ENDPOINTS
# =============================================================================


@router.post("/services", response_model=ServiceRegistryInDB, status_code=201)
async def create_service(
    service_in: ServiceRegistryCreate, db: AsyncSession = Depends(get_async_db)
):
    """Create a new service in the registry."""
    crud = get_service_registry_crud()
    existing = await crud.get_by_name(db, service_in.name)
    if existing:
        raise HTTPException(status_code=400, detail="Service already exists")
    service_in.status = ServiceStatus.ACTIVE
    service_in.last_health_check = datetime.now()
    return await crud.create(db, obj_in=service_in)


@router.get("/services", response_model=List[ServiceRegistryInDB])
async def list_services(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_db)
):
    """List all services with pagination."""
    crud = get_service_registry_crud()
    return await crud.get_multi(db, skip=skip, limit=limit)


@router.get("/services/{service_id}", response_model=ServiceRegistryInDB)
async def get_service(service_id: int, db: AsyncSession = Depends(get_async_db)):
    """Get a specific service by ID."""
    crud = get_service_registry_crud()
    db_obj = await crud.get(db, service_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Service not found")
    return db_obj


@router.put("/services/{service_id}", response_model=ServiceRegistryInDB)
async def update_service(
    service_id: int,
    service_in: ServiceRegistryUpdate,
    db: AsyncSession = Depends(get_async_db),
):
    """Update an existing service."""
    crud = get_service_registry_crud()
    db_obj = await crud.get(db, service_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Service not found")
    return await crud.update(db, db_obj=db_obj, obj_in=service_in)


@router.delete("/services/{service_id}", status_code=204)
async def delete_service(service_id: int, db: AsyncSession = Depends(get_async_db)):
    """Delete a service from the registry."""
    crud = get_service_registry_crud()
    db_obj = await crud.get(db, service_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Service not found")
    await crud.remove(db, service_id)
    return None


# =============================================================================
# EXTRA ENDPOINTS: ACTIVATE / DEACTIVATE / FORWARD
# =============================================================================


@router.post("/services/{service_id}/activate", response_model=ServiceRegistryInDB)
async def activate_service(service_id: int, db: AsyncSession = Depends(get_async_db)):
    """Activate a service by ID."""
    crud = get_service_registry_crud()
    db_obj = await crud.get(db, service_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Service not found")
    db_obj.status = ServiceStatus.ACTIVE
    db_obj.last_health_check = datetime.now()
    return await crud.update(db, db_obj=db_obj, obj_in=ServiceRegistryUpdate())


@router.post("/services/{service_id}/deactivate", response_model=ServiceRegistryInDB)
async def deactivate_service(service_id: int, db: AsyncSession = Depends(get_async_db)):
    """Deactivate a service by ID."""
    crud = get_service_registry_crud()
    db_obj = await crud.get(db, service_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Service not found")
    db_obj.status = ServiceStatus.INACTIVE
    return await crud.update(db, db_obj=db_obj, obj_in=ServiceRegistryUpdate())


@router.post("/services/{service_id}/forward", response_model=Dict)
async def forward_request(
    service_id: int, payload: Dict, db: AsyncSession = Depends(get_async_db)
):
    """Forward a request payload to the service endpoint."""
    crud = get_service_registry_crud()
    db_obj = await crud.get(db, service_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Service not found")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(db_obj.endpoint, json=payload)
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Forwarding failed: {str(e)}")
