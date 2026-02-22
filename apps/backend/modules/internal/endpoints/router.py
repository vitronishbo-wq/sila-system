# modules/internal/endpoints/router.py
from fastapi import APIRouter

router = APIRouter(prefix="/internal", tags=["internal"])


@router.get("/ping")
async def ping() -> dict[str, str]:
    """Health check do módulo internal (admin tasks)."""
    return {"status": "ok"}