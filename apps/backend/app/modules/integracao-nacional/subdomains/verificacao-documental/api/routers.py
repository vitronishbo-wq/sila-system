from ..api.health import router as health_router
from .router import router as verificacao_router

routers = [health_router, verificacao_router]
