from fastapi import APIRouter
router = APIRouter(prefix='/comercializacao-florestal', tags=['Florestas - Comercializacao Florestal'])

@router.get('/')
async def list_items() -> list[dict[str, str]]:
    return []