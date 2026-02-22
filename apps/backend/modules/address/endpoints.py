from fastapi import APIRouter

router = APIRouter()


@router.get("/address/ping")
async def ping():
    return {"status": "ok", "module": "address"}
