from ..api.health import router as health_router
from .router import router as moradas_router

routers = [health_router, moradas_router]
