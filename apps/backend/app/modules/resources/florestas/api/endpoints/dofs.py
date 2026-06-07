from fastapi import APIRouter

router = APIRouter(prefix="/dofs", tags=["Florestas - Dofs"])


@router.get("/")
async def list_items() -> list[dict[str, str]]:
    return []
