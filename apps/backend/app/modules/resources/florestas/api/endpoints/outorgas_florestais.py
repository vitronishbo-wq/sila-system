from fastapi import APIRouter

router = APIRouter(prefix="/outorgas-florestais", tags=["Florestas - Outorgas Florestais"])


@router.get("/")
async def list_items() -> list[dict[str, str]]:
    return []
