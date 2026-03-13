from apps.backend.app.modules.industry.domain.api.endpoints.catalogos import router as catalogos_router
from apps.backend.app.modules.industry.domain.api.endpoints.estabelecimentos_industriais import (
    router as estabelecimentos_industriais_router,
)

__all__ = ["catalogos_router", "estabelecimentos_industriais_router"]
