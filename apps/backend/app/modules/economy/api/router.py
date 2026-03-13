from fastapi import APIRouter

from apps.backend.app.modules.procurement.api.router import router as procurement_router
from apps.backend.app.modules.economy.public_budget.api.router import router as public_budget_router

router = APIRouter(prefix='/economy', tags=['economy'])

@router.get('/ping')
async def ping() -> dict[str, str]:
    return {'module': 'economy', 'status': 'ok'}


router.include_router(public_budget_router)
router.include_router(procurement_router)
