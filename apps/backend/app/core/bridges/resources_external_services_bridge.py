"""Bridge for resources module adapters that depend on external service factories."""

from apps.backend.app.modules.economy.industria.api.deps import (
    get_estabelecimento_industrial_service,
)
from apps.backend.app.modules.economy.trade.external.api.deps import get_exportador_service
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.api.deps import (
    get_imovel_service,
)

__all__ = ["get_estabelecimento_industrial_service", "get_exportador_service", "get_imovel_service"]
