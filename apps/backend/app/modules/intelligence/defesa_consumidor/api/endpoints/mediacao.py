from fastapi import APIRouter

router = APIRouter(prefix="/mediacao", tags=["Defesa Consumidor - Mediacao"])


@router.get("/ping")
async def ping() -> dict:
    return {"status": "ok", "message": "pong", "module": "defesa_consumidor.mediacao"}
