from fastapi import APIRouter

router = APIRouter(prefix="/integracao-nacional/nif", tags=["nif"])


@router.get("/health")
async def health():
    return {"status": "ok", "subdomain": "nif", "version": "1.0.0"}
