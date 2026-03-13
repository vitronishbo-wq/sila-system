from fastapi import APIRouter
router = APIRouter(prefix='/empresas-florestais', tags=['Florestas - Empresas Florestais'])

@router.get('/')
async def list_items() -> list[dict[str, str]]:
    return []