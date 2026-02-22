from fastapi import APIRouter

router = APIRouter()


@router.get("/social/ping")
async def ping():
    return {"status": "ok", "module": "social"}
