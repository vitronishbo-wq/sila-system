from fastapi import APIRouter
from app.modules.public_security.api.endpoints import cadeias_custodia_router, evidencias_router, investigacoes_router, laudos_periciais_router, mandados_router, ocorrencias_router, policiais_router, provas_periciais_router, unidades_policiais_router, vestigios_router
router = APIRouter(prefix='/seguranca-publica', tags=['Seguranca Publica'])
router.include_router(unidades_policiais_router)
router.include_router(policiais_router)
router.include_router(ocorrencias_router)
router.include_router(mandados_router)
router.include_router(investigacoes_router)
router.include_router(provas_periciais_router)
router.include_router(cadeias_custodia_router)
router.include_router(laudos_periciais_router)
router.include_router(vestigios_router)
router.include_router(evidencias_router)