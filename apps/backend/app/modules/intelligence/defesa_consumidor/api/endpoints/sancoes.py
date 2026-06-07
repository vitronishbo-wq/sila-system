from fastapi import APIRouter

router = APIRouter(prefix="/sancoes", tags=["Defesa Consumidor - Sancoes"])


@router.get("/ping")
async def ping() -> dict:
    return {"status": "ok", "message": "pong", "module": "defesa_consumidor.sancoes"}
