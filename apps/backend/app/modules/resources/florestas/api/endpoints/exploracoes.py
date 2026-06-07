from fastapi import APIRouter

router = APIRouter(prefix="/exploracoes", tags=["Florestas - Exploracoes"])


@router.get("/")
async def list_items() -> list[dict[str, str]]:
    return []
