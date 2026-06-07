from apps.backend.app.modules.society.desporto.api.endpoints.atletas import router as atletas_router
from apps.backend.app.modules.society.desporto.api.endpoints.clubes import router as clubes_router
from apps.backend.app.modules.society.desporto.api.endpoints.competicoes import (
    router as competicoes_router,
)
from apps.backend.app.modules.society.desporto.api.endpoints.estadios import (
    router as estadios_router,
)
from apps.backend.app.modules.society.desporto.api.endpoints.jogos import router as jogos_router

__all__ = [
    "atletas_router",
    "competicoes_router",
    "clubes_router",
    "jogos_router",
    "estadios_router",
]
