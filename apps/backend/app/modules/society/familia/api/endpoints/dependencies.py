from fastapi import APIRouter

router = APIRouter(prefix="/dependencies", tags=["Familia - Dependencies"])


@router.get("/health")
async def dependencies_health() -> dict:
    return {"status": "ok", "resource": "dependencies"}
