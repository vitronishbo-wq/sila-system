from fastapi import APIRouter
router = APIRouter(prefix='/autos-infracao-florestais', tags=['Florestas - Autos Infracao Florestais'])

@router.get('/')
async def list_items() -> list[dict[str, str]]:
    return []