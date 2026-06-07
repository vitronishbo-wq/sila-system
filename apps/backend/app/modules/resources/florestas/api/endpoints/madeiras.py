from fastapi import APIRouter

router = APIRouter(prefix="/madeiras", tags=["Florestas - Madeiras"])


@router.get("/")
async def list_items() -> list[dict[str, str]]:
    return []
