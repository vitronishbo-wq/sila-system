from fastapi import APIRouter
router = APIRouter(prefix='/projetos-carbono', tags=['Florestas - Projetos Carbono'])

@router.get('/')
async def list_items() -> list[dict[str, str]]:
    return []