from fastapi import APIRouter

router = APIRouter(prefix="/focos-calor", tags=["Florestas - Focos Calor"])


@router.get("/")
async def list_items() -> list[dict[str, str]]:
    return []
