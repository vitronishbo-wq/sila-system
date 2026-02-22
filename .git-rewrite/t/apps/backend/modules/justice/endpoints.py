from fastapi import APIRouter

router = APIRouter()


@router.get("/justice/ping")
async def ping():
    return {"status": "ok", "module": "justice"}
