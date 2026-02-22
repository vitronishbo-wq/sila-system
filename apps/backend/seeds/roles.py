import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.iam.models.permissions import Permission
from app.core.constants import UserRole
from app.core.database import AsyncSessionLocal

async def seed_roles_permissions(session: AsyncSession):
    print("Seeding roles & permissions...")
    
    permissions = [
        # Admin Central - Full Access
        Permission(role=UserRole.ADMIN_CENTRAL.value, service_code="BI_EMISSAO", can_read=True, can_write=True, can_approve=True),
        Permission(role=UserRole.ADMIN_CENTRAL.value, service_code="REG_NASCIMENTO", can_read=True, can_write=True, can_approve=True),
        Permission(role=UserRole.ADMIN_CENTRAL.value, service_code="FIN_PAGAMENTO", can_read=True, can_write=True, can_approve=True),
        
        # Manager/Provincial - Limited Approval
        Permission(role=UserRole.ADMIN_PROVINCIAL.value, service_code="BI_EMISSAO", can_read=True, can_write=True, can_approve=False),
        Permission(role=UserRole.ADMIN_PROVINCIAL.value, service_code="REG_NASCIMENTO", can_read=True, can_write=True, can_approve=False),
    ]
    
    try:
        session.add_all(permissions)
        await session.commit()
    except Exception as e:
        print(f"FAILED ROLES SEED: {e}")
        # Print details of the exception
        if hasattr(e, 'orig'):
             print(f"ORIGINAL ERROR: {e.orig}")
        raise
    
    print("✅ Roles & permissions seeded.")

if __name__ == "__main__":
    async def main():
        async with AsyncSessionLocal() as session:
            await seed_roles_permissions(session)
    asyncio.run(main())
