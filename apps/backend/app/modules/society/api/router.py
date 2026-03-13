from fastapi import APIRouter
router = APIRouter(prefix='/society', tags=['society'])

@router.get('/ping')
async def ping() -> dict[str, str]:
    return {'module': 'society', 'status': 'ok'}