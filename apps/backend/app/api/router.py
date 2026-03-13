from fastapi import APIRouter
api_router = APIRouter()
try:
    from app.presentation.api.citizen_routes import router as citizen_router
    api_router.include_router(citizen_router)
except Exception:
    pass
try:
    from app.presentation.api.citizen_document_routes import router as citizen_documents_router
    api_router.include_router(citizen_documents_router)
except Exception:
    pass