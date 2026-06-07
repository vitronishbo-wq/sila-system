from fastapi import APIRouter

router = APIRouter(prefix="/produtos-florestais", tags=["Florestas - Produtos Florestais"])


@router.get("/")
async def list_items() -> list[dict[str, str]]:
    return []
