import logging
from fastapi import APIRouter, Depends, HTTPException
from apps.backend.app.api.deps import get_current_user, get_db
from apps.backend.app.modules.justice.bounded_contexts.application.services.death_service import DeathService
logger = logging.getLogger('sila.registo_civil.api')
router = APIRouter(prefix='/death', tags=['Registo Civil - Eventos'])

def get_death_service(db=Depends(get_db)):
    from apps.backend.app.modules.justice.bounded_contexts.infrastructure.repositories.death_repository import DeathRepository
    from apps.backend.app.modules.justice.bounded_contexts.integrations.fuc_client import FUCClient
    return DeathService(DeathRepository(db), FUCClient())

@router.post('/')
async def register_death(payload: dict, service: DeathService=Depends(get_death_service), current_user=Depends(get_current_user)):
    """Registra um assento de óbito."""
    logger.info(f'Registrando óbito do cidadão: {payload.get('citizen_id')}')
    try:
        result = await service.register(payload)
        logger.info(f'Óbito registrado com sucesso: {result.get('death_certificate_id')}')
        return result
    except Exception as e:
        logger.error(f'Erro ao registrar óbito: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))