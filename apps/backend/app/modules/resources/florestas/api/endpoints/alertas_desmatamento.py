from fastapi import APIRouter
router = APIRouter(prefix='/alertas-desmatamento', tags=['Florestas - Alertas Desmatamento'])

@router.get('/')
async def list_items() -> list[dict[str, str]]:
    return []