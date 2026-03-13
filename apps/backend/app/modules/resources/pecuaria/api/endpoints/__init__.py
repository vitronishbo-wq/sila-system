from app.modules.resources.pecuaria.api.endpoints.animais import router as animais_router
from app.modules.resources.pecuaria.api.endpoints.pecuaristas import router as pecuaristas_router
from app.modules.resources.pecuaria.api.endpoints.producao import router as producao_router
from app.modules.resources.pecuaria.api.endpoints.propriedades import router as propriedades_router
from app.modules.resources.pecuaria.api.endpoints.rebanhos import router as rebanhos_router
from app.modules.resources.pecuaria.api.endpoints.sanidade import router as sanidade_router
__all__ = ['pecuaristas_router', 'propriedades_router', 'rebanhos_router', 'animais_router', 'producao_router', 'sanidade_router']