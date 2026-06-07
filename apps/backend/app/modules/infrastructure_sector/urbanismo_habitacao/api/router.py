from fastapi import APIRouter

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.endpoints import (
    licencas_urbanisticas_router,
    loteamentos_router,
    operacoes_urbanas_router,
    parcelamentos_router,
    planos_diretores_router,
    zoneamento_router,
)

router = APIRouter(prefix="/urbanismo-habitacao", tags=["Urbanismo Habitacao"])
router.include_router(planos_diretores_router)
router.include_router(zoneamento_router)
router.include_router(operacoes_urbanas_router)
router.include_router(parcelamentos_router)
router.include_router(loteamentos_router)
router.include_router(licencas_urbanisticas_router)
