from fastapi import APIRouter

router = APIRouter(prefix="/integracao-nacional/verificacao-documental", tags=["verificacao-documental"])


@router.get("/health")
async def health():
    return {"status": "ok", "subdomain": "verificacao-documental", "version": "1.0.0"}
