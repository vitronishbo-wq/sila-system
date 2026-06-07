from __future__ import annotations

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.core.db import get_db

db_dep = Depends(get_db)

from apps.backend.app.modules.intelligence.bi.application.services.dashboard_service import (
    DashboardService,
)
from apps.backend.app.modules.intelligence.bi.application.services.kpi_service import KPIService
from apps.backend.app.modules.intelligence.bi.integrations.data_sources import DataSources


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
        _ = permission
        return user

    return _dep


def get_data_sources(session: AsyncSession = db_dep) -> DataSources:
    return DataSources.from_session(session)

data_sources_dep = Depends(get_data_sources)


def get_dashboard_service(
    data_sources: DataSources = data_sources_dep,
) -> DashboardService:
    return DashboardService(data_sources=data_sources)


def get_kpi_service(data_sources: DataSources = data_sources_dep) -> KPIService:
    return KPIService(data_sources=data_sources)
