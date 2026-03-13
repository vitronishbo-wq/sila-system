from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.domain.db import get_db
from ..infrastructure.repositories.statistics_repository import StatisticsRepository
from ..application.services.statistics_service import StatisticsService
from ..integrations.data_sources import DataSources
from ..kpis_service import KPIService

def get_current_user(token: str=Depends(lambda: 'dev-token')):
    if not token:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return token

def require_permission(permission: str):

    def _dep(user=Depends(get_current_user)):
        return user
    return _dep

def get_statistics_repository(session: AsyncSession=Depends(get_db)) -> StatisticsRepository:
    """Dependency: Get Statistics Repository instance"""
    return StatisticsRepository(session)

def get_statistics_service(session: AsyncSession=Depends(get_db)) -> StatisticsService:
    """Dependency: Get Statistics Service instance"""
    repository = StatisticsRepository(session)
    sources = DataSources.from_session(session).as_dict()
    return StatisticsService(repository, data_sources=sources)

def get_kpi_service(session: AsyncSession=Depends(get_db)) -> KPIService:
    """Dependency: Get KPI Service with runtime wiring."""
    stats_service = get_statistics_service(session)
    return KPIService(db=session, stats_service=stats_service)