from fastapi import APIRouter

from apps.backend.app.modules.resources.pescas.industrial.api.endpoints import (
    armadores_industriais_router,
    certificacoes_router,
    embarcacoes_industriais_router,
    estatisticas_router,
    exportacoes_industriais_router,
    frigorificos_router,
    inspecoes_sanitarias_router,
    licencas_operacao_router,
    lotes_producao_router,
    produtos_processados_router,
    rastreabilidade_router,
    unidades_processamento_router,
)

router = APIRouter(prefix="/pescas-industriais", tags=["Pescas Industriais"])
router.include_router(armadores_industriais_router)
router.include_router(embarcacoes_industriais_router)
router.include_router(unidades_processamento_router)
router.include_router(frigorificos_router)
router.include_router(produtos_processados_router)
router.include_router(lotes_producao_router)
router.include_router(rastreabilidade_router)
router.include_router(certificacoes_router)
router.include_router(exportacoes_industriais_router)
router.include_router(inspecoes_sanitarias_router)
router.include_router(licencas_operacao_router)
router.include_router(estatisticas_router)
