from apps.backend.app.modules.resources.ambiente.api.endpoints.autos_infracao import (
    router as autos_infracao_router,
)
from apps.backend.app.modules.resources.ambiente.api.endpoints.car import router as car_router
from apps.backend.app.modules.resources.ambiente.api.endpoints.condicionantes import (
    router as condicionantes_router,
)
from apps.backend.app.modules.resources.ambiente.api.endpoints.embargos import (
    router as embargos_router,
)
from apps.backend.app.modules.resources.ambiente.api.endpoints.estudos import (
    router as estudos_router,
)
from apps.backend.app.modules.resources.ambiente.api.endpoints.fiscalizacoes import (
    router as fiscalizacoes_router,
)
from apps.backend.app.modules.resources.ambiente.api.endpoints.licencas import (
    router as licencas_router,
)
from apps.backend.app.modules.resources.ambiente.api.endpoints.multas import router as multas_router

__all__ = [
    "car_router",
    "licencas_router",
    "estudos_router",
    "condicionantes_router",
    "fiscalizacoes_router",
    "autos_infracao_router",
    "embargos_router",
    "multas_router",
]
