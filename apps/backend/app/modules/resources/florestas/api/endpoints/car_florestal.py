from fastapi import APIRouter

router = APIRouter(prefix="/car-florestal", tags=["Florestas - Car Florestal"])


@router.get("/")
async def list_items() -> list[dict[str, str]]:
    return []
