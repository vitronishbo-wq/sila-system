from fastapi import APIRouter

router = APIRouter(prefix="/relationships", tags=["Familia - Relationships"])


@router.get("/health")
async def relationships_health() -> dict:
    return {"status": "ok", "resource": "relationships"}
