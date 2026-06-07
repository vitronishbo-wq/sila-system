from fastapi import APIRouter

from apps.backend.app.modules.resources.agricultura.api.endpoints import (
    assistencia_router,
    certificacoes_router,
    colheitas_router,
    comercializacao_router,
    creditos_router,
    culturas_router,
    equipamentos_router,
    estoques_router,
    fitossanidade_router,
    insumos_router,
    operacoes_router,
    plantios_router,
    produtores_router,
    propriedades_router,
    safras_router,
    talhoes_router,
    zoneamento_router,
)

router = APIRouter(prefix="/agricultura", tags=["Agricultura"])
router.include_router(produtores_router)
router.include_router(propriedades_router)
router.include_router(culturas_router)
router.include_router(safras_router)
router.include_router(insumos_router)
router.include_router(estoques_router)
router.include_router(operacoes_router)
router.include_router(fitossanidade_router)
router.include_router(talhoes_router)
router.include_router(plantios_router)
router.include_router(colheitas_router)
router.include_router(equipamentos_router)
router.include_router(certificacoes_router)
router.include_router(comercializacao_router)
router.include_router(creditos_router)
router.include_router(assistencia_router)
router.include_router(zoneamento_router)
