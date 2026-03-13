from fastapi import APIRouter
router = APIRouter(prefix='/monitoramentos-satelite', tags=['Florestas - Monitoramentos Satelite'])

@router.get('/')
async def list_items() -> list[dict[str, str]]:
    return []