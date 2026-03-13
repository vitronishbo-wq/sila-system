from fastapi import APIRouter
router = APIRouter(prefix='/projections', tags=['Familia - Projections'])

@router.get('/health')
async def projections_health() -> dict:
    return {'status': 'ok', 'resource': 'projections'}