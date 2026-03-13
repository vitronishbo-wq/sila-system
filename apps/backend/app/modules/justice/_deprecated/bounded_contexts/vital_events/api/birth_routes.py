import logging
from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_current_user, get_db
from apps.backend.app.modules.justice.bounded_contexts.application.services.birth_service import BirthService
logger = logging.getLogger('sila.registo_civil.api')
router = APIRouter(prefix='/birth', tags=['Registo Civil - Eventos'])

def get_birth_service(db=Depends(get_db)):
    from apps.backend.app.modules.justice.bounded_contexts.infrastructure.repositories.birth_repository import BirthRepository
    from apps.backend.app.modules.justice.bounded_contexts.integrations.fuc_client import FUCClient
    return BirthService(BirthRepository(db), FUCClient())

@router.post('/')
async def register_birth(payload: dict, service: BirthService=Depends(get_birth_service), current_user=Depends(get_current_user)):
    """Registra um evento de nascimento (Normal ou Tardio)."""
    logger.info(f'Recebida requisição de registro de nascimento: {payload.get('nub')}')
    try:
        result = await service.register(payload)
        logger.info(f'Nascimento registrado com sucesso: {result.get('citizen_id')}')
        return result
    except Exception as e:
        logger.error(f'Erro ao registrar nascimento: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))