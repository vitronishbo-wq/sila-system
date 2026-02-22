from fastapi import APIRouter

router = APIRouter()


@router.get("/identity/ping")
async def ping():
    return {"status": "ok", "module": "identity"}
