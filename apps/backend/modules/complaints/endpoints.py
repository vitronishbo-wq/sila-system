from fastapi import APIRouter

router = APIRouter()


@router.get("/complaints/ping")
async def ping():
    return {"status": "ok", "module": "complaints"}
