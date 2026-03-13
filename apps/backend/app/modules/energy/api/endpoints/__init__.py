from apps.backend.app.modules.energy.api.endpoints.central_geradora import router as central_geradora_router
from apps.backend.app.modules.energy.api.endpoints.consumo import router as consumo_router
from apps.backend.app.modules.energy.api.endpoints.faturas import router as faturas_router
from apps.backend.app.modules.energy.api.endpoints.geracao import router as geracao_router
from apps.backend.app.modules.energy.api.endpoints.linha_transmissao import router as linha_transmissao_router
from apps.backend.app.modules.energy.api.endpoints.subestacao import router as subestacao_router
from apps.backend.app.modules.energy.api.endpoints.usinas import router as usinas_router
__all__ = ['usinas_router', 'central_geradora_router', 'subestacao_router', 'linha_transmissao_router', 'geracao_router', 'consumo_router', 'faturas_router']
