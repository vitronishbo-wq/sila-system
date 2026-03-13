import logging
from fastapi import APIRouter, Depends, HTTPException
from app.modules.justice.bounded_contexts.application.services.certificate_service import CertificateService
logger = logging.getLogger('sila.registo_civil.api')
router = APIRouter(tags=['Registo Civil - Certidões'])

def get_cert_service():
    return CertificateService()

@router.get('/{type}/{id}')
async def issue_certificate(type: str, id: str, service: CertificateService=Depends(get_cert_service)):
    """Emite diversos tipos de certidões (Nascimento, Casamento, Óbito, Estado Civil)."""
    logger.info(f'Solicitada emissão de certidão tipo {type} para ID {id}')
    try:
        if type == 'birth':
            return await service.issue_birth_certificate(id)
        elif type == 'marriage':
            return await service.issue_marriage_certificate(id)
        elif type == 'death':
            return await service.issue_death_certificate(id)
        elif type == 'civil-state':
            return await service.issue_civil_state_certificate(id)
        elif type == 'non-marriage':
            return await service.issue_non_marriage_certificate(id)
        else:
            raise HTTPException(status_code=400, detail='Tipo de certidão inválido')
    except Exception as e:
        logger.error(f'Erro na emissão de certidão: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))