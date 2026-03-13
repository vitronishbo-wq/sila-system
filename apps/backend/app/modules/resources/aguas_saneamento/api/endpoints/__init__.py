from apps.backend.app.modules.resources.aguas_saneamento.api.endpoints.abastecimento import router as abastecimento_router
from apps.backend.app.modules.resources.aguas_saneamento.api.endpoints.consumo import router as consumo_router
from apps.backend.app.modules.resources.aguas_saneamento.api.endpoints.faturas import router as faturas_router
from apps.backend.app.modules.resources.aguas_saneamento.api.endpoints.infraestrutura import router as infraestrutura_router
from apps.backend.app.modules.resources.aguas_saneamento.api.endpoints.outorgas import router as outorgas_router
__all__ = ['outorgas_router', 'infraestrutura_router', 'abastecimento_router', 'consumo_router', 'faturas_router']