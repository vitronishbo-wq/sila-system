from fastapi import APIRouter
router = APIRouter(prefix='/redds', tags=['Florestas - Redds'])

@router.get('/')
async def list_items() -> list[dict[str, str]]:
    return []