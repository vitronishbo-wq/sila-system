from fastapi import APIRouter

router = APIRouter()


@router.get("/reports/ping")
async def ping():
    return {"status": "ok", "module": "reports"}
