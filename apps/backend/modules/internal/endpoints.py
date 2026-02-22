from fastapi import APIRouter

router = APIRouter()


@router.get("/internal/ping")
async def ping():
    return {"status": "ok", "module": "internal"}
