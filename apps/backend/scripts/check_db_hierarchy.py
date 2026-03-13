import asyncio
from sqlalchemy import select
from config.database import AsyncSessionLocal
from apps.backend.app.modules.location.models.region import Region
from sqlalchemy.orm import selectinload


async def check_hierarchy():
    async with AsyncSessionLocal() as session:
        print("\n🔍 Verificando Hierarquia de Localização (DPA 2024)...")

        # 1. Buscar o País
        stmt = select(Region).where(Region.type == "PAIS").options(selectinload(Region.children))
        result = await session.execute(stmt)
        countries = result.scalars().all()

        for country in countries:
            print(f"\n🌍 [PAIS] ID: {country.id} | Nome: {country.name}")

            # 2. Buscar Províncias deste país
            stmt_p = select(Region).where(Region.parent_id ==
                                          country.id, Region.type == "PROVINCIA")
            res_p = await session.execute(stmt_p)
            provinces = res_p.scalars().all()

            print(f"   ┗ Total de Províncias: {len(provinces)}")

            # Mostrar todas as províncias e seus municípios como amostra
            for prov in provinces:
                print(f"      📍 [PROVINCIA] ID: {prov.id} | Nome: {prov.name}")

                stmt_m = select(Region).where(Region.parent_id ==
                                              prov.id, Region.type == "MUNICIPIO")
                res_m = await session.execute(stmt_m)
                municipalities = res_m.scalars().all()

                for mun in municipalities[:2]:  # Amostra de 2 municípios
                    print(
                        f"         • [MUNICIPIO] ID: {mun.id} | Nome: {mun.name} (Parent: {mun.parent_id})")

if __name__ == "__main__":
    asyncio.run(check_hierarchy())
