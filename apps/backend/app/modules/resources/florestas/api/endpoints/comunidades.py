from fastapi import APIRouter
router = APIRouter(prefix='/comunidades', tags=['Florestas - Comunidades'])

@router.get('/')
async def list_items() -> list[dict[str, str]]:
    return []