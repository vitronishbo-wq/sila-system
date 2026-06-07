from fastapi import APIRouter

router = APIRouter(prefix="/exportacoes-madeira", tags=["Florestas - Exportacoes Madeira"])


@router.get("/")
async def list_items() -> list[dict[str, str]]:
    return []
