from fastapi import APIRouter
router = APIRouter(prefix='/viveiros', tags=['Florestas - Viveiros'])

@router.get('/')
async def list_items() -> list[dict[str, str]]:
    return []