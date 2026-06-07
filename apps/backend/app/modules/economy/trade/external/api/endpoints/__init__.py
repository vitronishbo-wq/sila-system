from __future__ import annotations

import importlib
import pkgutil
from collections.abc import Iterable

from fastapi import APIRouter


def get_endpoint_routers() -> list[APIRouter]:
    routers: list[tuple[str, APIRouter]] = []
    for module in pkgutil.iter_modules(__path__):
        name = module.name
        if name.startswith("_"):
            continue
        mod = importlib.import_module(f"{__name__}.{name}")
        router = getattr(mod, "router", None)
        if isinstance(router, APIRouter):
            routers.append((name, router))
    routers.sort(key=lambda item: item[0])
    return [router for _, router in routers]


def iter_endpoint_modules() -> Iterable[str]:
    for module in pkgutil.iter_modules(__path__):
        name = module.name
        if not name.startswith("_"):
            yield name


from apps.backend.app.modules.economy.trade.external.api.endpoints.agente_carga import (
    router as agentes_carga_router,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints.cancelamento_radar import (
    router as cancelamento_radar_router,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints.despachante import (
    router as despachantes_router,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints.drawback import (
    router as drawback_router,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints.drawback_externo import (
    router as drawback_externo_router,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints.drawback_integrado import (
    router as drawback_integrado_router,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints.drawback_interno import (
    router as drawback_interno_router,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints.drawback_isencao import (
    router as drawback_isencao_router,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints.drawback_restituicao import (
    router as drawback_restituicao_router,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints.drawback_substituicao import (
    router as drawback_substituicao_router,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints.drawback_suspensao import (
    router as drawback_suspensao_router,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints.drawback_verde_amarelo import (
    router as drawback_verde_amarelo_router,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints.exportadores import (
    router as exportadores_router,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints.habilitacao_exportador import (
    router as habilitacoes_exportador_router,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints.habilitacao_importador import (
    router as habilitacoes_importador_router,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints.habilitacao_radar import (
    router as habilitacao_radar_router,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints.importador import (
    router as importadores_router,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints.radar import (
    router as radar_router,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints.siscomex_drawback import (
    router as siscomex_drawback_router,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints.suspensao_radar import (
    router as suspensao_radar_router,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints.transportador_internacional import (
    router as transportadores_internacionais_router,
)

__all__ = [
    "get_endpoint_routers",
    "iter_endpoint_modules",
    "agentes_carga_router",
    "cancelamento_radar_router",
    "despachantes_router",
    "drawback_router",
    "drawback_externo_router",
    "drawback_interno_router",
    "drawback_isencao_router",
    "drawback_integrado_router",
    "drawback_restituicao_router",
    "drawback_substituicao_router",
    "drawback_suspensao_router",
    "drawback_verde_amarelo_router",
    "siscomex_drawback_router",
    "exportadores_router",
    "habilitacoes_exportador_router",
    "habilitacoes_importador_router",
    "habilitacao_radar_router",
    "importadores_router",
    "radar_router",
    "suspensao_radar_router",
    "transportadores_internacionais_router",
]
