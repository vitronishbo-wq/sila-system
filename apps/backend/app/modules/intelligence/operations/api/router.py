from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_identity_context
from app.domain.identity import IdentityContext
from apps.backend.app.modules.intelligence.operations.api.deps import get_operations_service
from apps.backend.app.modules.intelligence.operations.api.schemas import OrderAttachDocumentsRequest, OrderCreateRequest, OrderResponse, PaymentResponse, ReceiptResponse, ServiceCatalogItemResponse
from apps.backend.app.modules.intelligence.operations.application.services.operations_service import OperationsService
router = APIRouter(tags=['Operational Flow'])

@router.get('/services', response_model=list[ServiceCatalogItemResponse])
async def list_services(service: OperationsService=Depends(get_operations_service)):
    return await service.list_services()

@router.post('/orders', response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(payload: OrderCreateRequest, service: OperationsService=Depends(get_operations_service), identity: IdentityContext=Depends(get_identity_context)):
    try:
        order = await service.create_order(identity.citizen_id(), payload.service_id)
        return order
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/orders/{order_id}', response_model=OrderResponse)
async def get_order(order_id: UUID, service: OperationsService=Depends(get_operations_service), identity: IdentityContext=Depends(get_identity_context)):
    try:
        return await service.get_order(order_id, identity.citizen_id())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.post('/orders/{order_id}/documents', response_model=OrderResponse)
async def attach_documents(order_id: UUID, payload: OrderAttachDocumentsRequest, service: OperationsService=Depends(get_operations_service), identity: IdentityContext=Depends(get_identity_context)):
    try:
        return await service.add_documents(order_id=order_id, citizen_id=identity.citizen_id(), documents=[doc.model_dump() for doc in payload.documents])
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/orders/{order_id}/submit', response_model=OrderResponse)
async def submit_order(order_id: UUID, service: OperationsService=Depends(get_operations_service), identity: IdentityContext=Depends(get_identity_context)):
    try:
        return await service.submit_order(order_id, identity.citizen_id())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/payments/{order_id}/generate', response_model=PaymentResponse)
async def generate_payment(order_id: UUID, service: OperationsService=Depends(get_operations_service), identity: IdentityContext=Depends(get_identity_context)):
    try:
        return await service.generate_payment(order_id, identity.citizen_id())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/payments/{reference}/confirm', response_model=PaymentResponse)
async def confirm_payment(reference: str, service: OperationsService=Depends(get_operations_service), _: IdentityContext=Depends(get_identity_context)):
    try:
        return await service.confirm_payment(reference)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/orders/{order_id}/complete', response_model=OrderResponse)
async def complete_order(order_id: UUID, service: OperationsService=Depends(get_operations_service), identity: IdentityContext=Depends(get_identity_context)):
    try:
        return await service.complete_order(order_id, identity.citizen_id())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/orders/{order_id}/receipt', response_model=ReceiptResponse)
async def get_receipt(order_id: UUID, service: OperationsService=Depends(get_operations_service), identity: IdentityContext=Depends(get_identity_context)):
    try:
        return await service.get_receipt(order_id, identity.citizen_id())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))