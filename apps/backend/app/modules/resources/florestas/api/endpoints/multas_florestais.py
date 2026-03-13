from fastapi import APIRouter
router = APIRouter(prefix='/multas-florestais', tags=['Florestas - Multas Florestais'])

@router.get('/')
async def list_items() -> list[dict[str, str]]:
    return []