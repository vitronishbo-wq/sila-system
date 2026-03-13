from fastapi import APIRouter
router = APIRouter(prefix='/arbitragem', tags=['Defesa Consumidor - Arbitragem'])

@router.get('/ping')
async def ping() -> dict:
    return {'status': 'ok', 'message': 'pong', 'module': 'defesa_consumidor.arbitragem'}