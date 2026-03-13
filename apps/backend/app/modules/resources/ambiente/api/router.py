from fastapi import APIRouter
from app.modules.resources.ambiente.api.endpoints import autos_infracao_router, car_router, condicionantes_router, embargos_router, estudos_router, fiscalizacoes_router, licencas_router, multas_router
router = APIRouter(prefix='/ambiente', tags=['Ambiente'])
router.include_router(car_router)
router.include_router(licencas_router)
router.include_router(estudos_router)
router.include_router(condicionantes_router)
router.include_router(fiscalizacoes_router)
router.include_router(autos_infracao_router)
router.include_router(embargos_router)
router.include_router(multas_router)