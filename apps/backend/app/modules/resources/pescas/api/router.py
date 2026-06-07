from fastapi import APIRouter

from apps.backend.app.modules.resources.pescas.api.endpoints import (
    armadores_router,
    capturas_router,
    comercializacao_router,
    defesos_router,
    desembarques_router,
    embarcacoes_router,
    especies_router,
    fiscalizacao_router,
    licencas_pesca_router,
    pescadores_router,
    producao_router,
    quotas_router,
    rastreabilidade_router,
)

router = APIRouter(prefix="/pescas", tags=["Pescas"])
router.include_router(pescadores_router)
router.include_router(armadores_router)
router.include_router(embarcacoes_router)
router.include_router(licencas_pesca_router)
router.include_router(capturas_router)
router.include_router(especies_router)
router.include_router(quotas_router)
router.include_router(defesos_router)
router.include_router(desembarques_router)
router.include_router(producao_router)
router.include_router(comercializacao_router)
router.include_router(fiscalizacao_router)
router.include_router(rastreabilidade_router)
