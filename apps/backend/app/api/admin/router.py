from fastapi import APIRouter
from app.api.admin.statistics.routes import router as stats_router
from app.api.admin.observability.routes import router as obs_router
from app.api.admin.observability.audit_routes import router as audit_router
from app.api.admin.services.routes import router as services_router
from app.api.admin.permissions.routes import router as permissions_router
from app.api.admin.territory.routes import router as territory_router
from app.api.admin.requests import router as requests_router
from app.api.admin.dashboard import router as dashboard_router

admin_router = APIRouter()
admin_router.include_router(stats_router)
admin_router.include_router(obs_router)
admin_router.include_router(audit_router)
admin_router.include_router(services_router)
admin_router.include_router(permissions_router)
admin_router.include_router(territory_router)
admin_router.include_router(requests_router)
admin_router.include_router(dashboard_router)
