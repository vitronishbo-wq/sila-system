from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.api.endpoints.desapropriacoes import (
    router as desapropriacoes_router,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.api.endpoints.georreferenciamentos import (
    router as georreferenciamentos_router,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.api.endpoints.imoveis import (
    router as imoveis_router,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.api.endpoints.matriculas import (
    router as matriculas_router,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.api.endpoints.oneracoes import (
    router as oneracoes_router,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.api.endpoints.proprietarios import (
    router as proprietarios_router,
)

__all__ = [
    "imoveis_router",
    "proprietarios_router",
    "oneracoes_router",
    "desapropriacoes_router",
    "matriculas_router",
    "georreferenciamentos_router",
]
