from app.modules.industry.core.api.endpoints.catalogos import router as catalogos_router
from app.modules.industry.core.api.endpoints.estabelecimentos_industriais import (
    router as estabelecimentos_industriais_router,
)

__all__ = ["catalogos_router", "estabelecimentos_industriais_router"]
