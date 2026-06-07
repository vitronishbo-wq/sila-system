from apps.backend.core.routers.health_factory import HealthRouterFactory

router = HealthRouterFactory.create_health_router(include_module=False)
