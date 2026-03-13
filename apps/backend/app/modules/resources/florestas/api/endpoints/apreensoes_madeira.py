from fastapi import APIRouter
router = APIRouter(prefix='/apreensoes-madeira', tags=['Florestas - Apreensoes Madeira'])

@router.get('/')
async def list_items() -> list[dict[str, str]]:
    return []