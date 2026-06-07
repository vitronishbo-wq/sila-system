from apps.backend.app.api.deps import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

db_dep = Depends(get_db)

from apps.backend.app.modules.intelligence.operations.application.services.operations_service import (
    OperationsService,
)


async def get_operations_service(db: AsyncSession = db_dep) -> OperationsService:
    return OperationsService(db)