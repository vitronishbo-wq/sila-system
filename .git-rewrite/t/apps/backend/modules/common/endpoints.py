from fastapi import APIRouter

router = APIRouter()


@router.get("/common/ping")
async def ping():
    return {"status": "ok", "module": "common"}
