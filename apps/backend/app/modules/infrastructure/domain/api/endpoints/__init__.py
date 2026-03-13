from app.modules.infrastructure.api.endpoints.dashboard import router as dashboard_router
from app.modules.infrastructure.api.endpoints.editais import router as editais_router
from app.modules.infrastructure.api.endpoints.licitacoes import router as licitacoes_router
from app.modules.infrastructure.api.endpoints.obras import router as obras_router
from app.modules.infrastructure.api.endpoints.projetos import router as projetos_router
__all__ = ['obras_router', 'projetos_router', 'licitacoes_router', 'editais_router', 'dashboard_router']
