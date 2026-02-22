from fastapi import APIRouter

router = APIRouter()


@router.get("/journeys/ping")
async def ping():
    return {"status": "ok", "module": "journeys"}
