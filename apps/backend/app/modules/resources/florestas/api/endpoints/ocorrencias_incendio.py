from fastapi import APIRouter

router = APIRouter(prefix="/ocorrencias-incendio", tags=["Florestas - Ocorrencias Incendio"])


@router.get("/")
async def list_items() -> list[dict[str, str]]:
    return []
