from fastapi import APIRouter
from app.modules.resources.pecuaria.api.endpoints import animais_router, pecuaristas_router, producao_router, propriedades_router, rebanhos_router, sanidade_router
router = APIRouter(prefix='/pecuaria', tags=['Pecuaria'])
router.include_router(pecuaristas_router)
router.include_router(propriedades_router)
router.include_router(rebanhos_router)
router.include_router(animais_router)
router.include_router(producao_router)
router.include_router(sanidade_router)