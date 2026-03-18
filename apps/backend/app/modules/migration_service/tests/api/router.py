from apps.backend.core.routers.router_factory import RouterFactory
from .health import router as health_router
router = RouterFactory.create_health_only_router(prefix='/migration-service-test', tags=['migration_service_tests'], health_router=health_router)