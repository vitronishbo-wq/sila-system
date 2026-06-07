from fastapi import APIRouter

router = APIRouter(prefix="/integracao-nacional/bi", tags=["bi"])


@router.get("/health")
async def health():
    return {"status": "ok", "subdomain": "bi", "version": "1.0.0"}
