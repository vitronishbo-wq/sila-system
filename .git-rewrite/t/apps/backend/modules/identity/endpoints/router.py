"""Identity router - minimal endpoints."""

from fastapi import APIRouter

router = APIRouter(tags=["Identity"])


@router.get("/ping")
async def ping():
    return {"status": "identity ok"}
