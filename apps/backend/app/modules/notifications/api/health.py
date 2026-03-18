from apps.backend.core.routers.health_factory import HealthRouterFactory
router = HealthRouterFactory.create_health_router(module_name='notifications')