from ..api.health import router as health_router
from apps.backend.app.modules.integracao-nacional.subdomains.nif.api.router import router as nif_router

routers = [health_router, nif_router]
