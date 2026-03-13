from fastapi import APIRouter
from app.modules.society.emprego.api.endpoints import candidatos_router, certificacoes_router, concursos_router, formacoes_router, mediacoes_router, ofertas_router, trabalhistas_router
router = APIRouter(prefix='/emprego', tags=['Emprego'])
router.include_router(candidatos_router)
router.include_router(ofertas_router)
router.include_router(mediacoes_router)
router.include_router(formacoes_router)
router.include_router(trabalhistas_router)
router.include_router(concursos_router)
router.include_router(certificacoes_router)