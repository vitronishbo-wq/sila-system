from apps.backend.app.modules.intelligence.ciencia_pesquisa.api.endpoints.instituicoes import (
    router as instituicoes_router,
)
from apps.backend.app.modules.intelligence.ciencia_pesquisa.api.endpoints.pesquisadores import (
    router as pesquisadores_router,
)
from apps.backend.app.modules.intelligence.ciencia_pesquisa.api.endpoints.projetos import (
    router as projetos_router,
)

__all__ = ["projetos_router", "pesquisadores_router", "instituicoes_router"]
