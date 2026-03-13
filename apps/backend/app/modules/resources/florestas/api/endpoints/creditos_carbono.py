from fastapi import APIRouter
router = APIRouter(prefix='/creditos-carbono', tags=['Florestas - Creditos Carbono'])

@router.get('/')
async def list_items() -> list[dict[str, str]]:
    return []