import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from sqlalchemy import select
from apps.backend.app.core.db import get_db
from apps.backend.app.modules.justice.bounded_contexts.permissions.access_control import AccessControlEngine
from apps.backend.app.modules.justice.bounded_contexts.permissions.policies import DataSegment
from apps.backend.app.modules.justice.bounded_contexts.events.models import CitizenEventModel
router = APIRouter(tags=['Citizen Platform Core'])

def verify_admin(service_id: str=Header(..., alias='X-Service-ID')):
    if service_id != 'ADMIN_CENTRAL':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Operação restrita à Administração Central do Estado (MAT).')
    return service_id

@router.get('/data/{citizen_id}/projection', summary='Consultar Projeção de Identidade', description='Recupera o estado atual (projeção) dos dados de identidade. Requer autorização IDENTITY:READ.')
def get_citizen_projection(citizen_id: uuid.UUID, service_id: str=Header(..., alias='X-Service-ID'), db: Session=Depends(get_db)):
    engine = AccessControlEngine(db)
    if not engine.check_authorization(service_id, DataSegment.IDENTITY, 'read'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"O serviço '{service_id}' não possui privilégios de leitura para o segmento IDENTITY.")
    query = select(CitizenEventModel).where(CitizenEventModel.citizen_id == citizen_id)
    result = db.execute(query).scalars().first()
    projection = result
    if not projection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cidadão não localizado no repositório de projeções.')
    return projection

@router.get('/data/{citizen_id}/events', summary='Consultar Histórico de Eventos', description='Recupera a memória jurídica filtrada por segmento. Requer autorização [SEGMENT]:READ.')
def get_citizen_events(citizen_id: uuid.UUID, segment: DataSegment, service_id: str=Header(..., alias='X-Service-ID'), db: Session=Depends(get_db)):
    engine = AccessControlEngine(db)
    if not engine.check_authorization(service_id, segment, 'read'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"O serviço '{service_id}' não possui privilégios para aceder ao segmento {segment}.")
    query = select(CitizenEventModel).where(CitizenEventModel.citizen_id == citizen_id)
    events = db.execute(query).scalars().all()
    return events