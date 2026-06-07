from fastapi import APIRouter

router = APIRouter(prefix="/reposicoes-florestais", tags=["Florestas - Reposicoes Florestais"])


@router.get("/")
async def list_items() -> list[dict[str, str]]:
    return []
