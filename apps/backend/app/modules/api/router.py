from fastapi import APIRouter
router = APIRouter(prefix='/', tags=[''])

@router.get('/ping')
async def ping() -> dict[str, str]:
    return {'module': '', 'status': 'ok'}