from fastapi import APIRouter
from apps.backend.app.modules.society.assistencia_social.api.endpoints import atendimentos_router, beneficiarios_router, beneficios_router, cadastros_unicos_router, criancas_risco_router, idosos_vulneraveis_router, pcd_router, programas_sociais_router, situacoes_rua_router, visitas_domiciliares_router
router = APIRouter(prefix='/assistencia-social', tags=['Assistencia Social'])
router.include_router(cadastros_unicos_router)
router.include_router(beneficiarios_router)
router.include_router(programas_sociais_router)
router.include_router(beneficios_router)
router.include_router(atendimentos_router)
router.include_router(visitas_domiciliares_router)
router.include_router(situacoes_rua_router)
router.include_router(criancas_risco_router)
router.include_router(idosos_vulneraveis_router)
router.include_router(pcd_router)