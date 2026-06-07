from apps.backend.app.modules.infrastructure_sector.aviacao_civil.api.endpoints.aeronaves import (
    router as aeronaves_router,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.api.endpoints.ocorrencias import (
    router as ocorrencias_router,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.api.endpoints.voos import (
    router as voos_router,
)

__all__ = ["aeronaves_router", "voos_router", "ocorrencias_router"]
