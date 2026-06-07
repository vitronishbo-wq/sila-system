from ..api.health import router as health_router
from apps.backend.app.modules.registo-civil.api.router import router as registo_router

routers = [health_router, registo_router]
