from apps.backend.app.api.deps import get_db, get_scope_from_user
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

db_dep = Depends(get_db)

from apps.backend.app.modules.intelligence.operations.application.services.operations_service import (
    OperationsService,
)


async def get_operations_service(
    db: AsyncSession = db_dep, scope: dict = Depends(get_scope_from_user)
) -> OperationsService:
    svc = OperationsService(db)
    try:
        svc.allowed_territories = scope.get("allowed_territories") if isinstance(scope, dict) else None
    except Exception:
        svc.allowed_territories = None
    return svc