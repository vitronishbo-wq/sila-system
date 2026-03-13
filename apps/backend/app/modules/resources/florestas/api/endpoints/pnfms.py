from fastapi import APIRouter
router = APIRouter(prefix='/pnfms', tags=['Florestas - Pnfms'])

@router.get('/')
async def list_items() -> list[dict[str, str]]:
    return []