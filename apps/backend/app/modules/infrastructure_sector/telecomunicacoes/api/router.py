from fastapi import APIRouter
from app.modules.infrastructure_sector.telecomunicacoes.api.endpoints import assinantes_router, espectros_router, faturas_router, indicadores_qualidade_router, infraestruturas_router, operadoras_router, outorgas_espectro_router, qualidade_servico_router, reclamacoes_router, slas_router
router = APIRouter(prefix='/telecomunicacoes', tags=['Telecomunicacoes'])
router.include_router(operadoras_router)
router.include_router(assinantes_router)
router.include_router(faturas_router)
router.include_router(reclamacoes_router)
router.include_router(infraestruturas_router)
router.include_router(outorgas_espectro_router)
router.include_router(espectros_router)
router.include_router(slas_router)
router.include_router(qualidade_servico_router)
router.include_router(indicadores_qualidade_router)