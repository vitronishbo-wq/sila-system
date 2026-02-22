"""Location Endpoints

This module defines the API endpoints for location management in the SILA system.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.session import get_db
from .models import CityModel, FullAddress
from .schemas import (
    CityResponse,
    FullAddressResponse,
    MunicipalityResponse,
    MunicipalityUpdate,
    ProvinceResponse,
    ProvinceUpdate,
)

router = APIRouter(tags=["locations"])


@router.get("/ping")
async def ping():
    """Health check for the location module."""
    return {"status": "ok", "module": "location"}


@router.get("/status")
async def status():
    """Status endpoint for the location module.

    Returns the current status of the location module including health and availability.
    """
    return {"status": "ok", "module": "location", "available": True, "version": "1.0.0"}


@router.get("/regions", response_model=List[ProvinceResponse])
async def get_regions(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """Get all regions."""
    return []


@router.post("/regions", status_code=501)
async def create_region(db: AsyncSession = Depends(get_db)):
    """Create a new region."""
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/regions/{region_id}", response_model=ProvinceResponse, status_code=501)
async def get_region(region_id: int, db: AsyncSession = Depends(get_db)):
    """Get a region by ID."""
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/regions/{region_id}", response_model=ProvinceResponse, status_code=501)
async def update_region(
    region_id: int, region_update: ProvinceUpdate, db: AsyncSession = Depends(get_db)
):
    """Update a region."""
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/regions/{region_id}", status_code=501)
async def delete_region(region_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a region."""
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/cities", response_model=List[CityResponse])
async def get_cities(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """Get all cities."""
    result = await db.execute(select(CityModel).offset(skip).limit(limit))
    cities = result.scalars().all()
    return [CityResponse.model_validate(c) for c in cities]


@router.post("/cities", status_code=501)
async def create_city(db: AsyncSession = Depends(get_db)):
    """Create a new city."""
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/cities/{city_id}", response_model=MunicipalityResponse, status_code=501)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    """Get a city by ID."""
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/cities/{city_id}", response_model=MunicipalityResponse, status_code=501)
async def update_city(
    city_id: int, city_update: MunicipalityUpdate, db: AsyncSession = Depends(get_db)
):
    """Update a city."""
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/cities/{city_id}", status_code=501)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a city."""
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/full-address/{address_id}", response_model=FullAddressResponse)
async def get_full_address(address_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a full address by ID."""
    result = await db.execute(select(FullAddress).where(FullAddress.id == address_id))
    address = result.scalars().first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return FullAddressResponse.model_validate(address)
