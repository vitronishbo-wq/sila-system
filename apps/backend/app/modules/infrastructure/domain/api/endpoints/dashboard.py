from __future__ import annotations
from fastapi import APIRouter, Depends, Header
from app.modules.infrastructure.api.deps import get_dashboard_query_service
from app.modules.infrastructure.api.schemas.obra_schema import ObraDashboardReadResponse
from app.modules.infrastructure.application.services.dashboard_query_service import DashboardQueryService
router = APIRouter(prefix='/dashboard', tags=['Obras Publicas - Dashboard'])

@router.get('/obras', response_model=list[ObraDashboardReadResponse])
async def listar_dashboard_obras(tenant_id: str | None=None, x_tenant_id: str | None=Header(default=None, alias='X-Tenant-ID'), query_service: DashboardQueryService=Depends(get_dashboard_query_service)):
    effective_tenant = (tenant_id or x_tenant_id or '').strip() or None
    return await query_service.listar_obras(tenant_id=effective_tenant)
