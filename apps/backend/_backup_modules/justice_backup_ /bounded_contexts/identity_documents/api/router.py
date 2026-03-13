from fastapi import APIRouter
from .bi_routes import router as bi_router
from .documents_routes import router as documents_router
router = APIRouter(prefix='/identity-documents', tags=['justice:identity-documents'])
router.include_router(bi_router)
router.include_router(documents_router)