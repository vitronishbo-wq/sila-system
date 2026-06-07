from fastapi import APIRouter

from apps.backend.app.modules.intelligence.defesa_consumidor.api.endpoints import (
    arbitragem_router,
    consumidores_router,
    estabelecimentos_router,
    mediacao_router,
    produtos_router,
    recalls_router,
    reclamacoes_router,
    sancoes_router,
)

router = APIRouter(prefix="/defesa_consumidor", tags=["Defesa Consumidor"])
router.include_router(reclamacoes_router)
router.include_router(consumidores_router)
router.include_router(estabelecimentos_router)
router.include_router(mediacao_router)
router.include_router(sancoes_router)
router.include_router(recalls_router)
router.include_router(arbitragem_router)
router.include_router(produtos_router)
