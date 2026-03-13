from fastapi import APIRouter
router = APIRouter(prefix='/especies-florestais', tags=['Florestas - Especies Florestais'])

@router.get('/')
async def list_items() -> list[dict[str, str]]:
    return []