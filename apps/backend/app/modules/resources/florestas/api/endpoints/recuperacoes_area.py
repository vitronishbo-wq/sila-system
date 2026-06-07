from fastapi import APIRouter

router = APIRouter(prefix="/recuperacoes-area", tags=["Florestas - Recuperacoes Area"])


@router.get("/")
async def list_items() -> list[dict[str, str]]:
    return []
