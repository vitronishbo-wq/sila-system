"""
Location Endpoints
Implementação completa dos endpoints de localização para o SILA system.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.session import get_async_db as get_db
from .repository import LocationRepository
from .schemas import (
    RegionResponse,
    RegionCreate,
    RegionUpdate,
    RegionTree,
    FullAddressResponse
)

router = APIRouter()

# --- Health & Status ---

@router.get("/status", tags=["Status"])
async def get_status():
    """Retorna o estado operacional do módulo de localização."""
    return {
        "status": "online",
        "module": "location",
        "version": "1.1.0",
        "features": ["recursive_tree", "data_scope_support"]
    }

# --- Regions (DPA Hierarchy) ---

@router.get("/tree", response_model=List[RegionTree])
async def get_location_tree(
    root_id: Optional[int] = None, 
    db: AsyncSession = Depends(get_db)
):
    """
    Retorna a árvore hierárquica (Província > Município > Comuna).
    Se root_id não for informado, retorna a árvore completa de Angola.
    """
    repo = LocationRepository(db)
    return await repo.get_region_tree(root_id)


@router.get("/regions", response_model=List[RegionResponse])
async def list_regions(
    parent_id: Optional[int] = None, 
    db: AsyncSession = Depends(get_db)
):
    """
    Lista regiões. Se parent_id for enviado, filtra subordinados diretos.
    Útil para seletores dinâmicos (Cascading Selects).
    """
    repo = LocationRepository(db)
    if parent_id:
        return await repo.get_subordinates(parent_id)
    return await repo.get_all_roots()


@router.post("/regions", response_model=RegionResponse, status_code=status.HTTP_201_CREATED)
async def create_region(payload: RegionCreate, db: AsyncSession = Depends(get_db)):
    """Cria uma nova entrada na Divisão Político-Administrativa."""
    repo = LocationRepository(db)
    return await repo.create_region(payload)


@router.get("/regions/{region_id}", response_model=RegionResponse)
async def get_region(region_id: int, db: AsyncSession = Depends(get_db)):
    """Busca detalhes de uma região específica."""
    repo = LocationRepository(db)
    region = await repo.get_region(region_id)
    if not region:
        raise HTTPException(status_code=404, detail="Região não encontrada")
    return region


@router.delete("/regions/{region_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_region(region_id: int, db: AsyncSession = Depends(get_db)):
    """Remove uma região e todos os seus descendentes (Cascade)."""
    repo = LocationRepository(db)
    success = await repo.delete_region(region_id)
    if not success:
        raise HTTPException(status_code=404, detail="Região não encontrada")
    return None

# --- Legacy Compatibility / Specifics ---

@router.get("/subordinates/{parent_id}", response_model=List[RegionResponse])
async def get_subordinates(parent_id: int, db: AsyncSession = Depends(get_db)):
    """Endpoint direto para buscar filhos de uma região (ex: municípios de uma província)."""
    repo = LocationRepository(db)
    return await repo.get_subordinates(parent_id)