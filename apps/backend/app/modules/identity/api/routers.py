"""API routers for Identity module"""
from apps.backend.core.routers.router_factory import RouterFactory
from .endpoints.qr_validator import router as qr_validator_router
from .endpoints.biometrics import router as biometrics_router

router = RouterFactory.create_module_router(module_name='Identity', prefix='/identity', tags=['Identity'])
router.include_router(qr_validator_router)
router.include_router(biometrics_router)
__all__ = ['router']
