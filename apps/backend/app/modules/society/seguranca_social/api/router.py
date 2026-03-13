from fastapi import APIRouter
from app.modules.society.seguranca_social.api.endpoints import beneficiarios_router, pensoes_router
router = APIRouter(prefix='/seguranca-social', tags=['Seguranca Social'])
router.include_router(beneficiarios_router)
router.include_router(pensoes_router)