from fastapi import APIRouter

router = APIRouter(
    prefix="/fiscalizacoes-florestais", tags=["Florestas - Fiscalizacoes Florestais"]
)


@router.get("/")
async def list_items() -> list[dict[str, str]]:
    return []
