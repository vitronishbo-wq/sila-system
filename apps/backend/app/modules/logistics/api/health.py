from apps.backend.core.routers.health_factory import HealthRouterFactory
router = HealthRouterFactory.create_inferred_health_router(module_path=__name__, infer_indices=(3, 4))