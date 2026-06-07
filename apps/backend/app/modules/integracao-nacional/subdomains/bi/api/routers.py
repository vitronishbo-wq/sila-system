from ..api.health import router as health_router
from apps.backend.app.modules.integracao-nacional.subdomains.bi.api.router import router as bi_router

routers = [health_router, bi_router]
