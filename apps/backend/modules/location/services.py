"""
Location Service Module

This module provides services for managing location entities:
Country, Province, Municipality, and Commune.
"""

import json
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.cache.redis import redis_client
from .models.hierarchy import ProvinceModel, MunicipalityModel, CommuneModel
from .schemas import (
    CommuneCreate,
    CommuneUpdate,
    CountryCreate,
    CountryResponse,
    CountryUpdate,
    MunicipalityCreate,
    MunicipalityResponse,
    MunicipalityUpdate,
    ProvinceCreate,
    ProvinceResponse,
    ProvinceUpdate,
    ProvinceTree,
)
from .models.region import Region


class LocationService:
    """Service for managing location entities."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_cached_location_tree(self) -> List[dict]:
        """
        Get the full location hierarchy tree (Province > Municipality > Commune).
        Uses Redis cache to optimize performance.
        """
        CACHE_KEY = "sila:location:tree:v1"
        CACHE_EXPIRE = 86400  # 24 hours

        # 1. Try to get from Redis
        try:
            cached_data = await redis_client.get(CACHE_KEY)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            # For now just print, but ideally use logger
            print(f"Redis cache error: {e}")

        # 2. If not found, get from DB
        query = (
            select(ProvinceModel)
            .options(
                selectinload(ProvinceModel.municipalities)
                .selectinload(MunicipalityModel.communes)
            )
            .order_by(ProvinceModel.name)
        )
        
        result = await self.db.execute(query)
        provinces = result.scalars().all()

        # 3. Serialize and save to Redis
        # Use ProvinceTree to serialize the nested structure
        tree_data = [
            ProvinceTree.model_validate(p).model_dump() 
            for p in provinces
        ]
        
        try:
            await redis_client.set(
                CACHE_KEY, 
                json.dumps(tree_data), 
                ex=CACHE_EXPIRE
            )
        except Exception as e:
            print(f"Redis set error: {e}")

        return tree_data

    async def get_region(self, region_id: int) -> Optional[dict]:
        """Get a region by ID."""
        result = await self.db.execute(select(Region).where(Region.id == region_id))
        db_region = result.scalars().first()
        if db_region:
            return {
                "id": db_region.id,
                "name": db_region.name,
                "type": db_region.type,
                "parent_id": db_region.parent_id,
            }
        return None

    async def list_regions(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """List all regions with pagination."""
        result = await self.db.execute(select(Region).offset(skip).limit(limit))
        db_regions = result.scalars().all()
        return [
            {
                "id": r.id,
                "name": r.name,
                "type": r.type,
                "parent_id": r.parent_id,
            }
            for r in db_regions
        ]

    async def create_region(self, region_data: dict) -> dict:
        """Create a new region."""
        db_region = Region(
            name=region_data.get("name"),
            type=region_data.get("type"),
            parent_id=region_data.get("parent_id"),
        )
        self.db.add(db_region)
        await self.db.commit()
        await self.db.refresh(db_region)
        return {
            "id": db_region.id,
            "name": db_region.name,
            "type": db_region.type,
            "parent_id": db_region.parent_id,
        }

    async def update_region(self, region_id: int, region_data: dict) -> Optional[dict]:
        """Update a region."""
        result = await self.db.execute(select(Region).where(Region.id == region_id))
        db_region = result.scalars().first()
        if not db_region:
            return None

        for field, value in region_data.items():
            if hasattr(db_region, field):
                setattr(db_region, field, value)

        await self.db.commit()
        await self.db.refresh(db_region)
        return {
            "id": db_region.id,
            "name": db_region.name,
            "type": db_region.type,
            "parent_id": db_region.parent_id,
        }

    async def delete_region(self, region_id: int) -> bool:
        """Delete a region."""
        result = await self.db.execute(select(Region).where(Region.id == region_id))
        db_region = result.scalars().first()
        if not db_region:
            return False
        await self.db.delete(db_region)
        await self.db.commit()
        return True
