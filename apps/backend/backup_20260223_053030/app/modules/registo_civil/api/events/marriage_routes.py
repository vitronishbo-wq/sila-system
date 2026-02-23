import logging
from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_current_user, get_db
from app.modules.registo_civil.application.services.marriage_service import MarriageService

logger = logging.getLogger("sila.registo_civil.api")
router = APIRouter(prefix="/marriage", tags=["Registo Civil - Eventos"])

def get_marriage_service(db=Depends(get_db)):
    from app.modules.registo_civil.infrastructure.repositories.marriage_repository import MarriageRepository
    from app.modules.registo_civil.integrations.fuc_client import FUCClient
    return MarriageService(MarriageRepository(db), FUCClient())

@router.post("/")
async def register_marriage(payload: dict, service: MarriageService = Depends(get_marriage_service), current_user = Depends(get_current_user)):
    """Registra um assento de casamento."""
    logger.info(f"Iniciando registro de casamento entre {payload.get('spouse1_id')} e {payload.get('spouse2_id')}")
    try:
        result = await service.register(payload)
        logger.info(f"Casamento registrado com sucesso: {result.get('marriage_id')}")
        return result
    except Exception as e:
        logger.error(f"Erro ao registrar casamento: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
