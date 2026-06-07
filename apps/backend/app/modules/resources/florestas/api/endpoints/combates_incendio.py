from fastapi import APIRouter

router = APIRouter(prefix="/combates-incendio", tags=["Florestas - Combates Incendio"])


@router.get("/")
async def list_items() -> list[dict[str, str]]:
    return []
