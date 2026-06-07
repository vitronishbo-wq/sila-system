from __future__ import annotations

from fastapi import APIRouter, Depends, Header

from apps.backend.app.modules.infrastructure.api.deps import get_dashboard_query_service
from apps.backend.app.modules.infrastructure.api.schemas.obra_schema import (
    ObraDashboardReadResponse,
)
from apps.backend.app.modules.infrastructure.application.services.dashboard_query_service import (
    DashboardQueryService,
)

router = APIRouter(prefix="/dashboard", tags=["Obras Publicas - Dashboard"])

x_tenant_id_header = Header(default=None, alias="X-Tenant-ID")
dashboard_query_service_dep = Depends(get_dashboard_query_service)


@router.get("/obras", response_model=list[ObraDashboardReadResponse])
async def listar_dashboard_obras(
    tenant_id: str | None = None,
    x_tenant_id: str | None = x_tenant_id_header,
    query_service: DashboardQueryService = dashboard_query_service_dep,
):
    effective_tenant = (tenant_id or x_tenant_id or "").strip() or None
    return await query_service.listar_obras(tenant_id=effective_tenant)