from fastapi import APIRouter
router = APIRouter(prefix='/incendios-florestais', tags=['Florestas - Incendios Florestais'])

@router.get('/')
async def list_items() -> list[dict[str, str]]:
    return []