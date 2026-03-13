from fastapi import APIRouter
router = APIRouter(prefix='/reservas-legais', tags=['Florestas - Reservas Legais'])

@router.get('/')
async def list_items() -> list[dict[str, str]]:
    return []