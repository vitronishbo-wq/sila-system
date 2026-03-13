from fastapi import APIRouter
router = APIRouter(prefix='/licencas-manejo', tags=['Florestas - Licencas Manejo'])

@router.get('/')
async def list_items() -> list[dict[str, str]]:
    return []