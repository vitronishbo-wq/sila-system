from fastapi import APIRouter

router = APIRouter(prefix="/produtos", tags=["Defesa Consumidor - Produtos"])


@router.get("/ping")
async def ping() -> dict:
    return {"status": "ok", "message": "pong", "module": "defesa_consumidor.produtos"}
