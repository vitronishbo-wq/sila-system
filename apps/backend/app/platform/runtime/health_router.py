from fastapi import APIRouter
router = APIRouter()

@router.get('/api/health/live')
def api_health_live():
    return {'alive': True}

@router.get('/api/health')
def api_health():
    return {'status': 'ok'}

@router.get('/system/health')
def system_health():
    return {'status': 'ok', 'system': 'SILA'}