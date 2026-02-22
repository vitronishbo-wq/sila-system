"""Internal router - minimal endpoints for admin tasks."""

from fastapi import APIRouter

router = APIRouter(tags=["Internal"])


@router.get("/ping")
async def ping():
    return {"status": "internal ok"}
