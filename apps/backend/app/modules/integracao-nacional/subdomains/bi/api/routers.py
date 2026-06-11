from ..api.health import router as health_router
from .router import router as bi_router

routers = [health_router, bi_router]
