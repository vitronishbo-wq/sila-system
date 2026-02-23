"""
Serviço de Territory - Lógica de query e busca
"""

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.territory.models.territory import Territory
from .schemas import TerritoryNode, TerritoryNodeWithChildren


class TerritoryService:
    """Serviço centralizado para operações de Territory"""

    @staticmethod
    async def get_provinces(db: AsyncSession) -> list[TerritoryNode]:
        """Lista todas as províncias"""
        query = select(Territory).where(Territory.type == "province").order_by(Territory.name)
        result = await db.execute(query)
        territories = result.scalars().all()
        return [TerritoryNode.from_orm(t) for t in territories]

    @staticmethod
    async def get_municipalities_by_province(
        db: AsyncSession, province_id: UUID
    ) -> list[TerritoryNode]:
        """Lista municípios de uma provência"""
        query = select(Territory).where(
            Territory.type == "municipality",
            Territory.parent_id == province_id
        ).order_by(Territory.name)
        result = await db.execute(query)
        territories = result.scalars().all()
        return [TerritoryNode.from_orm(t) for t in territories]

    @staticmethod
    async def get_communes_by_municipality(
        db: AsyncSession, municipality_id: UUID
    ) -> list[TerritoryNode]:
        """Lista comunas de um município"""
        query = select(Territory).where(
            Territory.type == "commune",
            Territory.parent_id == municipality_id
        ).order_by(Territory.name)
        result = await db.execute(query)
        territories = result.scalars().all()
        return [TerritoryNode.from_orm(t) for t in territories]

    @staticmethod
    async def get_territory_by_id(db: AsyncSession, territory_id: UUID) -> Territory | None:
        """Busca um território por ID"""
        query = select(Territory).where(Territory.id == territory_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_hierarchy_tree(db: AsyncSession) -> list[TerritoryNodeWithChildren]:
        """Retorna árvore completa (províncias com municípios com comunas)"""
        query = select(Territory).where(Territory.type == "province").order_by(Territory.name)
        result = await db.execute(query)
        provinces = result.scalars().all()

        tree = []
        for province in provinces:
            prov_dict = TerritoryNode.from_orm(province).dict()

            # Buscar municípios
            mun_query = select(Territory).where(
                Territory.type == "municipality",
                Territory.parent_id == province.id
            ).order_by(Territory.name)
            mun_result = await db.execute(mun_query)
            municipalities = mun_result.scalars().all()

            prov_dict["children"] = []
            for municipality in municipalities:
                mun_dict = TerritoryNode.from_orm(municipality).dict()

                # Buscar comunas
                com_query = select(Territory).where(
                    Territory.type == "commune",
                    Territory.parent_id == municipality.id
                ).order_by(Territory.name)
                com_result = await db.execute(com_query)
                communes = com_result.scalars().all()

                mun_dict["children"] = [TerritoryNode.from_orm(c).dict() for c in communes]
                prov_dict["children"].append(mun_dict)

            tree.append(TerritoryNodeWithChildren(**prov_dict))

        return tree
