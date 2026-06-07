from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.core.db import get_db

db_dep = Depends(get_db)


from ..application.services.statistics_service import StatisticsService
from ..infrastructure.repositories.statistics_repository import StatisticsRepository
from ..integrations.data_sources import DataSources
from ..kpis_service import KPIService


def _get_dev_token() -> str:
    return "dev-token"


dev_token_dep = Depends(_get_dev_token)


def get_current_user(token: str = dev_token_dep):
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token


def require_permission(permission: str):
    current_user_dep = Depends(get_current_user)

    def _dep(user=current_user_dep):
        return user

    return _dep


def get_statistics_repository(session: AsyncSession = db_dep) -> StatisticsRepository:
    """Dependency: Get Statistics Repository instance"""
    return StatisticsRepository(session)


def get_statistics_service(session: AsyncSession = db_dep) -> StatisticsService:
    """Dependency: Get Statistics Service instance"""
    repository = StatisticsRepository(session)
    sources = DataSources.from_session(session).as_dict()
    return StatisticsService(repository, data_sources=sources)


def get_kpi_service(session: AsyncSession = db_dep) -> KPIService:
    """Dependency: Get KPI Service with runtime wiring."""
    stats_service = get_statistics_service(session)
    return KPIService(db=session, stats_service=stats_service)
