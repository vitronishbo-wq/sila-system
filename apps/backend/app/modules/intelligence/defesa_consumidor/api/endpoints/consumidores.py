from fastapi import APIRouter
router = APIRouter(prefix='/consumidores', tags=['Defesa Consumidor - Consumidores'])

@router.get('/ping')
async def ping() -> dict:
    return {'status': 'ok', 'message': 'pong', 'module': 'defesa_consumidor.consumidores'}