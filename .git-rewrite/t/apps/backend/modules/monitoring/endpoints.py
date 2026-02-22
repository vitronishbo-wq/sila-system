from fastapi import APIRouter

router = APIRouter()


@router.get("/monitoring/ping")
async def ping():
    return {"status": "ok", "module": "monitoring"}
