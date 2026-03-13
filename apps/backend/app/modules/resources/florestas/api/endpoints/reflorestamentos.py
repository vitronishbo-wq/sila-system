from fastapi import APIRouter
router = APIRouter(prefix='/reflorestamentos', tags=['Florestas - Reflorestamentos'])

@router.get('/')
async def list_items() -> list[dict[str, str]]:
    return []