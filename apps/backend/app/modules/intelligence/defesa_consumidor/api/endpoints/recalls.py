from fastapi import APIRouter
router = APIRouter(prefix='/recalls', tags=['Defesa Consumidor - Recalls'])

@router.get('/ping')
async def ping() -> dict:
    return {'status': 'ok', 'message': 'pong', 'module': 'defesa_consumidor.recalls'}