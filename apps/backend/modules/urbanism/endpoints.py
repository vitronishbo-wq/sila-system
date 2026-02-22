from fastapi import APIRouter

router = APIRouter()


@router.get("/urbanism/ping")
async def ping():
    return {"status": "ok", "module": "urbanism"}
