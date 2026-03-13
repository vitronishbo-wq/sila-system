from fastapi import APIRouter
router = APIRouter(prefix='/history', tags=['Familia - History'])

@router.get('/health')
async def history_health() -> dict:
    return {'status': 'ok', 'resource': 'history'}