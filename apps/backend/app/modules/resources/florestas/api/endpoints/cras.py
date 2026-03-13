from fastapi import APIRouter
router = APIRouter(prefix='/cras', tags=['Florestas - Cras'])

@router.get('/')
async def list_items() -> list[dict[str, str]]:
    return []