import asyncio
import sys
from app.core.db import AsyncSessionLocal

from seeds.core.seed_angola_provinces import seed_territories
from seeds.catalog import seed_catalog
from seeds.core.seed_founding_users_with_territories import seed_roles_permissions
from seeds.core.seed_fuc_citizen import seed_citizens
from seeds.core.seed_founding_users import seed_users

async def run_all():
    print("🚀 Starting full database seed...")
    
    async with AsyncSessionLocal() as session:
        try:
            from sqlalchemy import text
            print("Cleaning core tables...")
            # Order to avoid FK issues with truncate
            tables = [
                "financas_payments", "financas_invoices", "financial_audit_logs",
                "processes", "requests", "documents", "notifications",
                "permissions", "users", "citizen_fuc", "territories",
                "services", "modules"
            ]
            for table in tables:
                await session.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))
            await session.commit()

            # Order is important for FKs
            await seed_territories(session)
            await seed_catalog(session)
            await seed_roles_permissions(session)
            await seed_citizens(session)
            await seed_users(session)
            
            print("✨ All seeds completed successfully!")
        except Exception as e:
            print(f"❌ Seed failed: {e}")
            import traceback
            traceback.print_exc()
            await session.rollback()
            sys.exit(1)

if __name__ == "__main__":
    asyncio.run(run_all())
