from app.modules.intelligence.defesa_consumidor.api.endpoints.arbitragem import router as arbitragem_router
from app.modules.intelligence.defesa_consumidor.api.endpoints.consumidores import router as consumidores_router
from app.modules.intelligence.defesa_consumidor.api.endpoints.estabelecimentos import router as estabelecimentos_router
from app.modules.intelligence.defesa_consumidor.api.endpoints.mediacao import router as mediacao_router
from app.modules.intelligence.defesa_consumidor.api.endpoints.produtos import router as produtos_router
from app.modules.intelligence.defesa_consumidor.api.endpoints.recalls import router as recalls_router
from app.modules.intelligence.defesa_consumidor.api.endpoints.reclamacoes import router as reclamacoes_router
from app.modules.intelligence.defesa_consumidor.api.endpoints.sancoes import router as sancoes_router
__all__ = ['arbitragem_router', 'consumidores_router', 'estabelecimentos_router', 'mediacao_router', 'produtos_router', 'recalls_router', 'reclamacoes_router', 'sancoes_router']