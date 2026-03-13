from fastapi import APIRouter
router = APIRouter(prefix='/desmatamentos-ilegais', tags=['Florestas - Desmatamentos Ilegais'])

@router.get('/')
async def list_items() -> list[dict[str, str]]:
    return []