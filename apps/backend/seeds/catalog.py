import asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.catalog.models.module import Module
from app.core.catalog.models.service import Service
from app.core.database import AsyncSessionLocal

async def seed_catalog(session: AsyncSession):
    print("Seeding catalog (modules & services)...")
    
async def seed_catalog(session: AsyncSession):
    print("Seeding catalog (modules & services)...")
    

    # 1. Modules
    identidade = Module(
        id=1,
        slug="identidade-civil",
        title="Identidade Civil",
        description="Emissão de Bilhete de Identidade e Cartão de Cidadão.",
        icon="🪪",
        color="#C8102E",
        is_active=True,
        is_foundational=True,
        order=1
    )
    registo = Module(
        id=2,
        slug="registo-civil",
        title="Registo Civil",
        description="Registos de nascimento, casamento e óbito.",
        icon="📜",
        color="#002366",
        is_active=True,
        is_foundational=True,
        order=2
    )
    financas = Module(
        id=3,
        slug="financas",
        title="Finanças",
        description="Pagamentos de emolumentos e taxas.",
        icon="💳",
        color="#006400",
        is_active=True,
        is_foundational=True,
        order=3
    )
    
    session.add_all([identidade, registo, financas])
    await session.flush() # Ensure IDs are available

    # 2. Services
    services = [
        # Identidade Civil
        Service(
            code="BI_EMISSAO",
            name="Emissão de Bilhete de Identidade",
            module_id=identidade.id,
            price=2500.00,
            estimated_days=7,
            is_public=True,
            is_essential=True,
            icon_slug="id-card"
        ),
        # Registo Civil
        Service(
            code="REG_NASCIMENTO",
            name="Registo de Nascimento",
            module_id=registo.id,
            price=0.00,
            estimated_days=3,
            is_public=True,
            is_essential=True,
            icon_slug="baby"
        ),
        # Finanças
        Service(
            code="FIN_PAGAMENTO",
            name="Pagamento de Taxas",
            module_id=financas.id,
            price=0.00,
            estimated_days=1,
            is_public=False,
            is_essential=False,
            icon_slug="credit-card"
        )
    ]
    
    session.add_all(services)
    await session.commit()
    print("✅ Catalog seeded.")

if __name__ == "__main__":
    async def main():
        async with AsyncSessionLocal() as session:
            await seed_catalog(session)
    asyncio.run(main())
