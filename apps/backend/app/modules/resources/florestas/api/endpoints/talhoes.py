from fastapi import APIRouter
router = APIRouter(prefix='/talhoes', tags=['Florestas - Talhoes'])

@router.get('/')
async def list_items() -> list[dict[str, str]]:
    return []