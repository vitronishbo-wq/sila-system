from ..api.health import router as health_router
from apps.backend.app.modules.integracao-nacional.subdomains.verificacao-documental.api.router import router as verif_router

routers = [health_router, verif_router]
