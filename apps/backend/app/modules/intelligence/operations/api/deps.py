from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.api.deps import get_db
from apps.backend.app.modules.intelligence.operations.application.services.operations_service import OperationsService

async def get_operations_service(db: AsyncSession=Depends(get_db)) -> OperationsService:
    return OperationsService(db)