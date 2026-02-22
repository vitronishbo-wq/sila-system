from fastapi import APIRouter

router = APIRouter(prefix="", tags=["Health"])

@router.get("/health")
async def health_check():
    """Health check endpoint - sempre retorna OK"""
    return {"status": "ok", "service": "SILA-System"}
