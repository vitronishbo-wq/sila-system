from fastapi import APIRouter

router = APIRouter()


@router.get("/commercial/ping")
async def ping():
    return {"status": "ok", "module": "commercial"}
