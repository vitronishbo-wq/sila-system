from fastapi import APIRouter
from apps.backend.app.modules.educacao.api.endpoints import boletins_router, certificados_router, concursos_router, emprego_router, formacoes_router, inscricoes_router, matricula_router, propinas_router, transferencias_router, universidade_router
router = APIRouter(prefix='/educacao', tags=['Educacao'])
router.include_router(matricula_router)
router.include_router(inscricoes_router)
router.include_router(boletins_router)
router.include_router(certificados_router)
router.include_router(transferencias_router)
router.include_router(propinas_router)
router.include_router(emprego_router)
router.include_router(concursos_router)
router.include_router(formacoes_router)
router.include_router(universidade_router)