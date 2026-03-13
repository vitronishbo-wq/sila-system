from fastapi import APIRouter
router = APIRouter(prefix='/certificacoes-florestais', tags=['Florestas - Certificacoes Florestais'])

@router.get('/')
async def list_items() -> list[dict[str, str]]:
    return []