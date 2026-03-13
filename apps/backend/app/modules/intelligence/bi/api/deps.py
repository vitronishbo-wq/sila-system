from __future__ import annotations
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.modules.intelligence.bi.application.services.dashboard_service import DashboardService
from app.modules.intelligence.bi.application.services.kpi_service import KPIService
from app.modules.intelligence.bi.integrations.data_sources import DataSources

def get_current_user(token: str=Depends(lambda: 'dev-token')):
    if not token:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return token

def require_permission(permission: str):

    def _dep(user=Depends(get_current_user)):
        _ = permission
        return user
    return _dep

def get_data_sources(session: AsyncSession=Depends(get_db)) -> DataSources:
    return DataSources.from_session(session)

def get_dashboard_service(data_sources: DataSources=Depends(get_data_sources)) -> DashboardService:
    return DashboardService(data_sources=data_sources)

def get_kpi_service(data_sources: DataSources=Depends(get_data_sources)) -> KPIService:
    return KPIService(data_sources=data_sources)