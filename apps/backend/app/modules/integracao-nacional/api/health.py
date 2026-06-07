from fastapi import APIRouter

router = APIRouter(prefix="/integracao-nacional", tags=["integracao-nacional"])


@router.get("/health")
async def health():
    return {"status": "ok", "module": "integracao-nacional", "version": "1.0.0"}
