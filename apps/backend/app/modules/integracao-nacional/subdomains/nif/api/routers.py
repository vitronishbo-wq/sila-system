from ..api.health import router as health_router
from .router import router as nif_router

routers = [health_router, nif_router]
