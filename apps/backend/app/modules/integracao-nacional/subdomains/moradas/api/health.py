from fastapi import APIRouter

router = APIRouter(prefix="/integracao-nacional/moradas", tags=["moradas"])


@router.get("/health")
async def health():
    return {"status": "ok", "subdomain": "moradas", "version": "1.0.0"}
