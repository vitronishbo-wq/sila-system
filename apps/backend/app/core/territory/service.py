"""Territory Management Service"""
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import Base

class TerritoryService:
    """Service for managing hierarchical territory relationships"""

    @staticmethod
    async def get_all_provinces(db: AsyncSession):
        """Retorna todas as províncias (locations com type='province' e parent_id=None)"""
        from app.core.models.location import Location
        result = await db.execute(select(Location).where(and_(Location.type == 'province', Location.parent_id == None)).order_by(Location.name))
        return result.scalars().all()

    @staticmethod
    async def get_province_by_id(db: AsyncSession, province_id: int):
        """Retorna uma província específica"""
        from app.core.models.location import Location
        result = await db.execute(select(Location).where(and_(Location.id == province_id, Location.type == 'province')))
        return result.scalars().first()

    @staticmethod
    async def get_municipalities_in_province(db: AsyncSession, province_id: int):
        """Retorna todos os municípios de uma província"""
        from app.core.models.location import Location
        result = await db.execute(select(Location).where(and_(Location.type == 'municipality', Location.parent_id == province_id)).order_by(Location.name))
        return result.scalars().all()

    @staticmethod
    async def get_communes_in_municipality(db: AsyncSession, municipality_id: int):
        """Retorna todas as comunas de um município"""
        from app.core.models.location import Location
        result = await db.execute(select(Location).where(and_(Location.type == 'commune', Location.parent_id == municipality_id)).order_by(Location.name))
        return result.scalars().all()

    @staticmethod
    async def get_full_hierarchy(db: AsyncSession, province_id: int):
        """
        Retorna a hierarquia completa de uma província:
        {
            province: {...},
            municipalities: [
                {
                    municipality: {...},
                    communes: [...]
                }
            ]
        }
        """
        from app.core.models.location import Location
        province_result = await db.execute(select(Location).where(Location.id == province_id))
        province = province_result.scalars().first()
        if not province:
            return None
        mun_result = await db.execute(select(Location).where(and_(Location.type == 'municipality', Location.parent_id == province_id)).order_by(Location.name))
        municipalities = mun_result.scalars().all()
        hierarchy = {'province': {'id': province.id, 'name': province.name, 'type': province.type}, 'municipalities': []}
        for mun in municipalities:
            comm_result = await db.execute(select(Location).where(and_(Location.type == 'commune', Location.parent_id == mun.id)).order_by(Location.name))
            communes = comm_result.scalars().all()
            hierarchy['municipalities'].append({'municipality': {'id': mun.id, 'name': mun.name, 'type': mun.type}, 'communes': [{'id': c.id, 'name': c.name, 'type': c.type} for c in communes]})
        return hierarchy

    @staticmethod
    async def get_territory_ancestors(db: AsyncSession, location_id: int):
        """Retorna todos os ancestrais de um local (comunidade -> município -> província)"""
        from app.core.models.location import Location
        ancestors = []
        current_id = location_id
        for _ in range(10):
            result = await db.execute(select(Location).where(Location.id == current_id))
            location = result.scalars().first()
            if not location:
                break
            ancestors.append({'id': location.id, 'name': location.name, 'type': location.type})
            if location.parent_id is None:
                break
            current_id = location.parent_id
        return ancestors