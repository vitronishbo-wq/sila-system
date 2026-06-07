from fastapi import APIRouter

router = APIRouter(prefix="/registo-civil", tags=["registo-civil"])


@router.get("/health")
async def health():
    return {"status": "ok", "module": "registo-civil", "version": "1.0.0"}
