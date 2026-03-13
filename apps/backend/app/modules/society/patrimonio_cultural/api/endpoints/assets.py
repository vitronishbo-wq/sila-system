from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from apps.backend.app.modules.society.patrimonio_cultural.api.deps import get_cultural_asset_service
from apps.backend.app.modules.society.patrimonio_cultural.api.schemas import ClassificationRequestSchema, CulturalAssetCreateSchema, CulturalAssetResponseSchema, CulturalEventSchema, PreservationActionSchema
from apps.backend.app.modules.society.patrimonio_cultural.application.services import CulturalAssetService
from apps.backend.app.modules.society.patrimonio_cultural.domain.enums import AssetStatus, AssetType, ClassificationLevel
from apps.backend.app.modules.society.patrimonio_cultural.domain.exceptions import AssetAlreadyClassifiedError, AssetNotFoundError, InvalidClassificationAuthorityError, UNESCOPreconditionError
router = APIRouter(prefix='/assets', tags=['Patrimonio Cultural - Assets'])

def _raise_400(exc: Exception) -> None:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

def _raise_404(exc: Exception) -> None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.post('/', response_model=CulturalAssetResponseSchema, status_code=status.HTTP_201_CREATED)
async def register_cultural_asset(payload: CulturalAssetCreateSchema, service: CulturalAssetService=Depends(get_cultural_asset_service)) -> dict:
    try:
        asset = await service.register_asset(name=payload.name, asset_type=payload.asset_type, province=payload.province, municipality=payload.municipality, latitude=payload.latitude, longitude=payload.longitude, altitude=payload.altitude, address=payload.address, description=payload.description, historical_period=payload.historical_period, cultural_significance=payload.cultural_significance, legal_reference=payload.legal_reference)
        return asset.to_dict()
    except ValueError as exc:
        _raise_400(exc)

@router.get('/', response_model=list[CulturalAssetResponseSchema])
async def list_cultural_assets(asset_type: AssetType | None=None, province: str | None=None, classification_level: ClassificationLevel | None=None, asset_status: AssetStatus | None=Query(default=None, alias='status'), limit: int=Query(default=100, ge=1, le=500), offset: int=Query(default=0, ge=0), service: CulturalAssetService=Depends(get_cultural_asset_service)) -> list[dict]:
    assets = await service.list_assets(asset_type=asset_type, province=province, classification_level=classification_level, status=asset_status, limit=limit, offset=offset)
    return [asset.to_dict() for asset in assets]

@router.get('/inventory')
async def get_cultural_inventory(province: str | None=None, classification_level: ClassificationLevel | None=None, include_events: bool=False, include_actions: bool=False, service: CulturalAssetService=Depends(get_cultural_asset_service)) -> list[dict]:
    return await service.get_asset_inventory(province=province, classification_level=classification_level, include_events=include_events, include_actions=include_actions)

@router.get('/protected/report')
async def get_protected_assets_report(province: str | None=None, service: CulturalAssetService=Depends(get_cultural_asset_service)) -> dict:
    return await service.get_protected_assets_report(province=province)

@router.get('/{asset_id}', response_model=CulturalAssetResponseSchema)
async def get_cultural_asset(asset_id: UUID, service: CulturalAssetService=Depends(get_cultural_asset_service)) -> dict:
    try:
        asset = await service.get_asset_by_id(asset_id)
        return asset.to_dict()
    except AssetNotFoundError as exc:
        _raise_404(exc)

@router.post('/{asset_id}/classification', response_model=CulturalAssetResponseSchema)
async def classify_cultural_asset(asset_id: UUID, payload: ClassificationRequestSchema, service: CulturalAssetService=Depends(get_cultural_asset_service)) -> dict:
    try:
        asset = await service.classify_asset(asset_id=asset_id, classification_level=payload.classification_level, authority=payload.authority, classification_date=payload.classification_date)
        return asset.to_dict()
    except AssetNotFoundError as exc:
        _raise_404(exc)
    except (ValueError, InvalidClassificationAuthorityError, UNESCOPreconditionError, AssetAlreadyClassifiedError) as exc:
        _raise_400(exc)

@router.post('/{asset_id}/preservation-actions', status_code=status.HTTP_201_CREATED)
async def add_preservation_action(asset_id: UUID, payload: PreservationActionSchema, service: CulturalAssetService=Depends(get_cultural_asset_service)) -> dict:
    try:
        action = await service.add_preservation_action(asset_id=asset_id, action_type=payload.action_type, description=payload.description, executed_by=payload.executed_by, action_date=payload.action_date, cost=payload.cost, funding_source=payload.funding_source)
        return action.to_dict()
    except AssetNotFoundError as exc:
        _raise_404(exc)
    except ValueError as exc:
        _raise_400(exc)

@router.post('/{asset_id}/events', status_code=status.HTTP_201_CREATED)
async def register_cultural_event(asset_id: UUID, payload: CulturalEventSchema, service: CulturalAssetService=Depends(get_cultural_asset_service)) -> dict:
    try:
        event = await service.register_cultural_event(asset_id=asset_id, name=payload.name, event_date=payload.event_date, organizer=payload.organizer, description=payload.description, expected_attendance=payload.expected_attendance, requires_authorization=payload.requires_authorization)
        return event.to_dict()
    except AssetNotFoundError as exc:
        _raise_404(exc)
    except ValueError as exc:
        _raise_400(exc)