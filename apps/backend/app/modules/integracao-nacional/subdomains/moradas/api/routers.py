from ..api.health import router as health_router
from apps.backend.app.modules.integracao-nacional.subdomains.moradas.api.router import router as moradas_router

routers = [health_router, moradas_router]
