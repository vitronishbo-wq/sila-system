from fastapi import APIRouter

router = APIRouter(prefix="/estabelecimentos", tags=["Defesa Consumidor - Estabelecimentos"])


@router.get("/ping")
async def ping() -> dict:
    return {"status": "ok", "message": "pong", "module": "defesa_consumidor.estabelecimentos"}
