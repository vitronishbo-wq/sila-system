from fastapi import APIRouter

router = APIRouter(prefix="/concessoes-florestais", tags=["Florestas - Concessoes Florestais"])


@router.get("/")
async def list_items() -> list[dict[str, str]]:
    return []
