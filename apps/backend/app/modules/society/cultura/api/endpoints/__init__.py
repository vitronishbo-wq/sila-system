from apps.backend.app.modules.society.cultura.api.endpoints.artistas import router as artistas_router
from apps.backend.app.modules.society.cultura.api.endpoints.bens_culturais import router as bens_culturais_router
from apps.backend.app.modules.society.cultura.api.endpoints.editais import router as editais_router
from apps.backend.app.modules.society.cultura.api.endpoints.espacos_culturais import router as espacos_culturais_router
from apps.backend.app.modules.society.cultura.api.endpoints.eventos_culturais import router as eventos_culturais_router
from apps.backend.app.modules.society.cultura.api.endpoints.grupos_artisticos import router as grupos_artisticos_router
from apps.backend.app.modules.society.cultura.api.endpoints.patrimonios_imateriais import router as patrimonios_imateriais_router
from apps.backend.app.modules.society.cultura.api.endpoints.projetos_culturais import router as projetos_culturais_router
__all__ = ['artistas_router', 'bens_culturais_router', 'espacos_culturais_router', 'projetos_culturais_router', 'editais_router', 'eventos_culturais_router', 'grupos_artisticos_router', 'patrimonios_imateriais_router']