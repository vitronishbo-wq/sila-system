from ..api.health import router as health_router
from .router import router as registo_router

routers = [health_router, registo_router]
