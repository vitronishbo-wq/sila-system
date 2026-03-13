from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from app.modules.society.familia.api.deps import get_family_aggregate_service, get_family_query_service
from app.modules.society.familia.api.schemas.family_aggregate_schema import FamilyAggregateCreateSchema, FamilyAggregateResponseSchema, FamilyDissolveSchema, FamilyMemberCreateSchema, FamilyTransferHeadSchema, FamilyTreeResponseSchema
from app.modules.society.familia.application.services.family_aggregate_service import FamilyAggregateService
from app.modules.society.familia.application.services.family_query_service import FamilyQueryService
from app.modules.society.familia.exceptions import to_http_error
router = APIRouter(prefix='/families', tags=['Familia - Aggregates'])

@router.post('', response_model=FamilyAggregateResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_family_aggregate(payload: FamilyAggregateCreateSchema, service: FamilyAggregateService=Depends(get_family_aggregate_service)) -> FamilyAggregateResponseSchema:
    try:
        return await service.create_aggregate(head_citizen_id=payload.head_citizen_id, initial_members=payload.members, metadata=payload.metadata)
    except Exception as exc:
        raise to_http_error(exc)

@router.get('/citizen/{citizen_id}', response_model=list[FamilyAggregateResponseSchema])
async def list_families_for_citizen(citizen_id: UUID, limit: int=Query(100, ge=1, le=500), offset: int=Query(0, ge=0), service: FamilyQueryService=Depends(get_family_query_service)) -> list[FamilyAggregateResponseSchema]:
    try:
        return await service.list_families_for_citizen(citizen_id, limit=limit, offset=offset)
    except Exception as exc:
        raise to_http_error(exc)

@router.get('/citizen/{citizen_id}/active', response_model=FamilyAggregateResponseSchema)
async def get_active_family_for_citizen(citizen_id: UUID, service: FamilyQueryService=Depends(get_family_query_service)) -> FamilyAggregateResponseSchema:
    try:
        return await service.get_active_family_for_citizen(citizen_id)
    except Exception as exc:
        raise to_http_error(exc)

@router.get('/citizen/{citizen_id}/dependents')
async def get_dependents_for_citizen(citizen_id: UUID, service: FamilyQueryService=Depends(get_family_query_service)) -> dict:
    try:
        result = await service.get_dependents_for_head(citizen_id)
        result['citizen_id'] = str(result['citizen_id'])
        return result
    except Exception as exc:
        raise to_http_error(exc)

@router.get('/{family_id}', response_model=FamilyAggregateResponseSchema)
async def get_family_aggregate(family_id: UUID, service: FamilyQueryService=Depends(get_family_query_service)) -> FamilyAggregateResponseSchema:
    try:
        return await service.get_aggregate(family_id)
    except Exception as exc:
        raise to_http_error(exc)

@router.get('/{family_id}/tree', response_model=FamilyTreeResponseSchema)
async def get_family_tree(family_id: UUID, service: FamilyQueryService=Depends(get_family_query_service)) -> FamilyTreeResponseSchema:
    try:
        return await service.get_family_tree(family_id)
    except Exception as exc:
        raise to_http_error(exc)

@router.post('/{family_id}/members', response_model=FamilyAggregateResponseSchema)
async def add_family_member(family_id: UUID, payload: FamilyMemberCreateSchema, service: FamilyAggregateService=Depends(get_family_aggregate_service)) -> FamilyAggregateResponseSchema:
    try:
        return await service.add_member_to_aggregate(family_id=family_id, citizen_id=payload.citizen_id, role=payload.role)
    except Exception as exc:
        raise to_http_error(exc)

@router.put('/{family_id}/transfer-head', response_model=FamilyAggregateResponseSchema)
async def transfer_family_head(family_id: UUID, payload: FamilyTransferHeadSchema, service: FamilyAggregateService=Depends(get_family_aggregate_service)) -> FamilyAggregateResponseSchema:
    try:
        return await service.transfer_head(family_id=family_id, new_head_citizen_id=payload.new_head_citizen_id)
    except Exception as exc:
        raise to_http_error(exc)

@router.delete('/{family_id}', response_model=FamilyAggregateResponseSchema)
async def dissolve_family_aggregate(family_id: UUID, payload: FamilyDissolveSchema, service: FamilyAggregateService=Depends(get_family_aggregate_service)) -> FamilyAggregateResponseSchema:
    try:
        return await service.dissolve_aggregate(family_id=family_id, reason=payload.reason)
    except Exception as exc:
        raise to_http_error(exc)