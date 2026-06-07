from fastapi import APIRouter

from apps.backend.app.modules.resources.aguas_saneamento.api.endpoints import (
    abastecimento_router,
    consumo_router,
    faturas_router,
    infraestrutura_router,
    outorgas_router,
)

router = APIRouter(prefix="/aguas-saneamento", tags=["Aguas Saneamento"])
router.include_router(outorgas_router)
router.include_router(infraestrutura_router)
router.include_router(abastecimento_router)
router.include_router(consumo_router)
router.include_router(faturas_router)
