from fastapi import APIRouter
router = APIRouter(prefix='/autorizacoes-supressao', tags=['Florestas - Autorizacoes Supressao'])

@router.get('/')
async def list_items() -> list[dict[str, str]]:
    return []