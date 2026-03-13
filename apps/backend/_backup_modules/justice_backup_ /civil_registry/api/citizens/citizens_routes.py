from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user, get_db
from app.models.iam_user import IamUser as User
from app.core.utils.dates import safe_isoformat
from app.core.utils.parsing import safe_get
from app.core.bridges.citizen_repository_bridge import CitizenRepository
from app.core.bridges.society_repository_bridges import make_assistencia_beneficiario_repository, make_educacao_matricula_repository, make_emprego_candidato_repository, make_juventude_jovem_repository, make_saude_medical_record_repository
from app.modules.justice.bounded_contexts.application.services.citizen_service import CitizenService
from app.modules.justice.bounded_contexts.infrastructure.adapters import AssistenciaSocialServiceAdapter, EducacaoServiceAdapter, EmpregoServiceAdapter, JuventudeServiceAdapter, SaudeServiceAdapter
from app.modules.justice.bounded_contexts.exceptions import NotFoundException, BusinessRuleException
router = APIRouter(prefix='/citizens', tags=['Citizens'])

class CitizenResponse(BaseModel):
    citizen_id: str
    document_number: Optional[str]
    full_name: str
    birth_date: Optional[date]
    gender: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    model_config = ConfigDict(from_attributes=True)

def get_citizen_repo(db: AsyncSession=Depends(get_db)) -> CitizenRepository:
    """Provedor de dependência para CitizenRepository."""
    return CitizenRepository(db)

def get_citizen_service(db: AsyncSession=Depends(get_db)) -> CitizenService:
    """Provedor de dependência para CitizenService com integrações cross-módulo."""
    educacao_service = EducacaoServiceAdapter(make_educacao_matricula_repository(db))
    juventude_service = JuventudeServiceAdapter(make_juventude_jovem_repository(db))
    emprego_service = EmpregoServiceAdapter(make_emprego_candidato_repository(db))
    saude_service = SaudeServiceAdapter(make_saude_medical_record_repository(db))
    assistencia_social_service = AssistenciaSocialServiceAdapter(make_assistencia_beneficiario_repository(db))
    return CitizenService(educacao_service=educacao_service, juventude_service=juventude_service, emprego_service=emprego_service, saude_service=saude_service, assistencia_social_service=assistencia_social_service)

@router.get('/', response_model=List[CitizenResponse])
async def list_citizens(skip: int=Query(0, ge=0), limit: int=Query(20, ge=1, le=100), current_user: User=Depends(get_current_user), repo: CitizenRepository=Depends(get_citizen_repo)):
    """Lista cidadãos do cache local com paginação."""
    citizens = await repo.list_all(limit=limit, offset=skip)
    return [CitizenResponse(citizen_id=str(c.citizen_id), document_number=safe_get(c, 'document_number'), full_name=c.full_name, birth_date=safe_get(c, 'birth_date'), gender=safe_get(c, 'gender'), phone=safe_get(c, 'phone'), email=safe_get(c, 'email')) for c in citizens]

@router.get('/search', response_model=List[CitizenResponse])
async def search_citizens(q: str=Query(..., min_length=2, description='Pesquisar por nome'), current_user: User=Depends(get_current_user), repo: CitizenRepository=Depends(get_citizen_repo)):
    """Pesquisa cidadãos por nome."""
    citizens = await repo.search_by_name(q)
    return [CitizenResponse(citizen_id=str(c.citizen_id), document_number=safe_get(c, 'document_number'), full_name=c.full_name, birth_date=safe_get(c, 'birth_date'), gender=safe_get(c, 'gender'), phone=safe_get(c, 'phone'), email=safe_get(c, 'email')) for c in citizens]

@router.get('/{citizen_id}')
async def get_citizen(citizen_id: str, current_user: User=Depends(get_current_user), repo: CitizenRepository=Depends(get_citizen_repo)):
    from uuid import UUID
    try:
        cid = UUID(citizen_id)
    except ValueError:
        raise BusinessRuleException('ID de cidadão inválido')
    citizen = await repo.get_by_id(cid)
    if not citizen:
        raise NotFoundException('Cidadão não encontrado')
    return {'citizen_id': str(citizen.citizen_id), 'document_number': safe_get(citizen, 'document_number'), 'full_name': citizen.full_name, 'birth_date': safe_isoformat(safe_get(citizen, 'birth_date')), 'gender': safe_get(citizen, 'gender'), 'phone': safe_get(citizen, 'phone'), 'email': safe_get(citizen, 'email'), 'nif': safe_get(citizen, 'nif'), 'province_id': str(safe_get(citizen, 'province_id')) if safe_get(citizen, 'province_id') else None, 'municipality_id': str(safe_get(citizen, 'municipality_id')) if safe_get(citizen, 'municipality_id') else None, 'current_address': safe_get(citizen, 'current_address'), 'vital_status': safe_get(citizen, 'vital_status'), 'created_at': safe_isoformat(safe_get(citizen, 'created_at')), 'updated_at': safe_isoformat(safe_get(citizen, 'updated_at'))}

@router.get('/{citizen_id}/completo')
async def get_citizen_completo(citizen_id: str, current_user: User=Depends(get_current_user), service: CitizenService=Depends(get_citizen_service)):
    """Obtém perfil completo do cidadão com dados enriquecidos de outros módulos."""
    _ = current_user
    result = await service.get_citizen_completo(citizen_id)
    if not result:
        raise NotFoundException('Cidadão não encontrado')
    return result