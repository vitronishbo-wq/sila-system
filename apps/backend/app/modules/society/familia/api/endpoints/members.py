from fastapi import APIRouter
router = APIRouter(prefix='/members', tags=['Familia - Members'])

@router.get('/health')
async def members_health() -> dict:
    return {'status': 'ok', 'resource': 'members'}