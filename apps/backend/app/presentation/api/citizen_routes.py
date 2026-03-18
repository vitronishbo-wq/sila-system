from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from uuid import UUID
from ..schemas.citizen_schema import CitizenCreateSchema, CitizenUpdateSchema, CitizenReadSchema
from ...application.citizen_service import CitizenService
from ...infrastructure.db.session import get_session
from apps.backend.app.core.bridges.citizen_repository_bridge import CitizenRepository
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter(prefix='/citizens', tags=['citizens'])

async def get_citizen_service(session: AsyncSession=Depends(get_session)):
    repo = CitizenRepository(session)
    return CitizenService(repo)

@router.post('/', response_model=CitizenReadSchema)
async def create_citizen(citizen_in: CitizenCreateSchema, service: CitizenService=Depends(get_citizen_service)):
    citizen = await service.create_citizen(citizen_in)
    return citizen

@router.patch('/{citizen_id}', response_model=CitizenReadSchema)
async def update_citizen(citizen_id: UUID, citizen_in: CitizenUpdateSchema, service: CitizenService=Depends(get_citizen_service)):
    citizen = await service.get_citizen_by_id(citizen_id)
    if not citizen:
        raise HTTPException(status_code=404, detail='Citizen not found')
    for field, value in citizen_in.dict(exclude_unset=True).items():
        setattr(citizen, field, value)
    updated = await service.update_citizen(citizen)
    return updated

@router.get('/{citizen_id}', response_model=CitizenReadSchema)
async def get_citizen_by_id(citizen_id: UUID, service: CitizenService=Depends(get_citizen_service)):
    citizen = await service.get_citizen_by_id(citizen_id)
    if not citizen:
        raise HTTPException(status_code=404, detail='Citizen not found')
    return citizen

@router.get('/by_bi/{bi}', response_model=CitizenReadSchema)
async def get_citizen_by_bi(bi: str, service: CitizenService=Depends(get_citizen_service)):
    citizen = await service.get_citizen_by_national_id_number(bi)
    if not citizen:
        raise HTTPException(status_code=404, detail='Citizen not found')
    return citizen

@router.get('/by_nif/{nif}', response_model=CitizenReadSchema)
async def get_citizen_by_nif(nif: str, service: CitizenService=Depends(get_citizen_service)):
    citizen = await service.get_citizen_by_nif(nif)
    if not citizen:
        raise HTTPException(status_code=404, detail='Citizen not found')
    return citizen

@router.get('/', response_model=List[CitizenReadSchema])
async def list_citizens(name: Optional[str]=Query(None), bi: Optional[str]=Query(None), nif: Optional[str]=Query(None), phone: Optional[str]=Query(None), province: Optional[str]=Query(None), birth_date: Optional[str]=Query(None), status: Optional[str]=Query(None), limit: int=Query(10, ge=1, le=100), offset: int=Query(0, ge=0), service: CitizenService=Depends(get_citizen_service)):
    filters = {'full_name': name, 'national_id_number': bi, 'nif': nif, 'phone': phone, 'province': province, 'birth_date': birth_date, 'status': status}
    citizens = await service.list_citizens(filters=filters, limit=limit, offset=offset)
    return citizens

@router.delete('/{citizen_id}')
async def soft_delete_citizen(citizen_id: UUID, service: CitizenService=Depends(get_citizen_service)):
    await service.soft_delete_citizen(citizen_id)
    return {'detail': 'Citizen soft deleted (status set to INACTIVE)'}