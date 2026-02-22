import logging
from typing import List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func

from modules.location.models.region import Region
from modules.location.schemas import RegionCreate, RegionUpdate

logger = logging.getLogger(__name__)

class LocationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_region(self, region_id: int) -> Optional[Region]:
        """Busca uma região específica pelo ID."""
        return await self.db.get(Region, region_id)

    async def get_all_roots(self) -> List[Region]:
        """Retorna apenas as regiões de nível superior (ex: País ou Províncias sem parent)."""
        result = await self.db.execute(
            select(Region).where(Region.parent_id == None).order_by(Region.name)
        )
        return list(result.scalars().all())

    async def get_region_tree(self, root_id: Optional[int] = None) -> List[Region]:
        """
        Retorna a hierarquia completa de regiões.
        Se root_id for fornecido, retorna a árvore a partir dali (ex: todos os municípios de uma província).
        Usa selectinload para evitar o problema de N+1 consultas.
        """
        query = select(Region).options(
            selectinload(Region.children).selectinload(Region.children)
        )
        
        if root_id:
            query = query.where(Region.id == root_id)
        else:
            query = query.where(Region.parent_id == None)
            
        result = await self.db.execute(query.order_by(Region.name))
        return list(result.scalars().all())

    async def create_region(self, payload: RegionCreate) -> Region:
        """Cria uma nova região (Província, Município ou Comuna)."""
        new_region = Region(
            name=payload.name,
            type=payload.type.upper(),
            parent_id=payload.parent_id
        )
        self.db.add(new_region)
        try:
            await self.db.commit()
            await self.db.refresh(new_region)
            return new_region
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Erro ao criar região: {e}")
            raise

    async def get_subordinates(self, parent_id: int) -> List[Region]:
        """Retorna apenas os filhos diretos de uma região."""
        result = await self.db.execute(
            select(Region).where(Region.parent_id == parent_id).order_by(Region.name)
        )
        return list(result.scalars().all())

    async def delete_region(self, region_id: int) -> bool:
        """Remove uma região (o cascade delete no model cuidará dos filhos)."""
        region = await self.get_region(region_id)
        if region:
            await self.db.delete(region)
            await self.db.commit()
            return True
        return False