from fastapi import APIRouter

router = APIRouter(prefix="/embargos-florestais", tags=["Florestas - Embargos Florestais"])


@router.get("/")
async def list_items() -> list[dict[str, str]]:
    return []
