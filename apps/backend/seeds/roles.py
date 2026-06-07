import asyncio

from apps.backend.app.core.constants import UserRole
from apps.backend.app.core.db import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

_permission_import_error = None
try:
    from apps.backend.app.modules.identity.infrastructure.models.permission_model import (
        PermissionModel as Permission,
    )
except Exception:
    try:
        from apps.backend.app.db.base import PermissionModel as Permission
    except Exception as inner_exc:
        Permission = None
        _permission_import_error = inner_exc


async def seed_roles_permissions(session: AsyncSession):
    print("Seeding roles & permissions...")
    if Permission is None:
        raise RuntimeError(
            "PermissionModel não disponível. core/iam foi removido e o seed precisa "
            "apontar para o novo modelo de permissões."
        ) from _permission_import_error

    permissions = [
        # Admin Central - Full Access
        Permission(
            role=UserRole.ADMIN_CENTRAL.value,
            service_code="BI_EMISSAO",
            can_read=True,
            can_write=True,
            can_approve=True,
        ),
        Permission(
            role=UserRole.ADMIN_CENTRAL.value,
            service_code="REG_NASCIMENTO",
            can_read=True,
            can_write=True,
            can_approve=True,
        ),
        Permission(
            role=UserRole.ADMIN_CENTRAL.value,
            service_code="FIN_PAGAMENTO",
            can_read=True,
            can_write=True,
            can_approve=True,
        ),
        # Manager/Provincial - Limited Approval
        Permission(
            role=UserRole.ADMIN_PROVINCIAL.value,
            service_code="BI_EMISSAO",
            can_read=True,
            can_write=True,
            can_approve=False,
        ),
        Permission(
            role=UserRole.ADMIN_PROVINCIAL.value,
            service_code="REG_NASCIMENTO",
            can_read=True,
            can_write=True,
            can_approve=False,
        ),
    ]

    try:
        session.add_all(permissions)
        await session.commit()
    except Exception as e:
        print(f"FAILED ROLES SEED: {e}")
        # Print details of the exception
        if hasattr(e, "orig"):
            print(f"ORIGINAL ERROR: {e.orig}")
        raise

    print("✅ Roles & permissions seeded.")


if __name__ == "__main__":

    async def main():
        async with AsyncSessionLocal() as session:
            await seed_roles_permissions(session)

    asyncio.run(main())
