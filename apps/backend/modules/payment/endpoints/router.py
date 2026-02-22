# modules/payment/endpoints/router.py
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status, Request, Header
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.session import get_async_db
from core.security import get_current_active_user  # Para uso futuro com autenticação real
from ..crud import PaymentCRUD, get_payment_crud
from ..models.enums import PaymentMethod, PaymentStatus, TransactionType
from ..schemas.payment import (
    PaymentCreate,
    PaymentFilter,
    PaymentResponse,
    PaymentUpdate,
    RefundCreate,
    RefundResponse,
    TransactionResponse,
)
from ..services.payment_service import PaymentService
from ..services.webhook_service import WebhookEngine
from config.settings import settings

router = APIRouter(prefix="/payments", tags=["payments"])


def get_payment_service(db: AsyncSession = Depends(get_async_db)) -> PaymentService:
    """Injeção do serviço de pagamento."""
    return PaymentService(db)


@router.get("/ping")
async def ping() -> dict:
    """Health check do módulo payments."""
    return {
        "status": "ok",
        "module": "payments",
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PaymentResponse)
async def create_payment(
    payment: PaymentCreate,
    crud: PaymentCRUD = Depends(get_payment_crud),
    current_user=Depends(get_current_active_user),  # Placeholder para auth real
):
    """Cria novo pagamento."""
    db_obj = await crud.create(payment, created_by=current_user.id if current_user else 1)
    return PaymentResponse.model_validate(db_obj)


@router.get("/", response_model=List[PaymentResponse])
async def list_payments(
    status: Optional[PaymentStatus] = Query(None),
    method: Optional[PaymentMethod] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    crud: PaymentCRUD = Depends(get_payment_crud),
):
    """Lista pagamentos com filtros opcionais."""
    filters = PaymentFilter(status=status, method=method)
    db_objs = await crud.get_filtered(filters, skip=skip, limit=limit)
    return [PaymentResponse.model_validate(obj) for obj in db_objs]


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(payment_id: int, crud: PaymentCRUD = Depends(get_payment_crud)):
    """Retorna detalhes de pagamento específico."""
    payment = await crud.get(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    return PaymentResponse.model_validate(payment)


@router.post("/{payment_id}/transaction", response_model=TransactionResponse)
async def create_transaction(
    payment_id: int,
    transaction_type: TransactionType,
    amount: Optional[float] = None,
    service: PaymentService = Depends(get_payment_service),
):
    """Registra nova transação para pagamento."""
    transaction = await service.create_transaction(
        payment_id=payment_id, transaction_type=transaction_type, amount=amount
    )
    return TransactionResponse.model_validate(transaction)


@router.post("/{payment_id}/refund", response_model=RefundResponse)
async def create_refund(
    payment_id: int,
    refund_data: RefundCreate,
    service: PaymentService = Depends(get_payment_service),
    current_user=Depends(get_current_active_user),
):
    """Processa pedido de reembolso."""
    refund = await service.create_refund(
        payment_id, refund_data, user_id=current_user.id if current_user else 1
    )
    return RefundResponse.model_validate(refund)


@router.get("/{payment_id}/receipt")
async def get_payment_receipt(
    payment_id: int,
    format: str = Query("pdf", pattern="^(pdf|json|html)$"),
    service: PaymentService = Depends(get_payment_service),
):
    """Gera e retorna recibo em formato solicitado."""
    receipt = await service.generate_receipt(payment_id, format=format)
    if not receipt:
        raise HTTPException(status_code=404, detail="Recibo não disponível")

    if format == "pdf":
        return FileResponse(
            receipt,
            media_type="application/pdf",
            filename=f"recibo_{payment_id}.pdf",
        )
    return receipt


@router.post("/webhook")
async def payment_webhook(
    request: Request,
    x_signature: str = Header(None, alias="X-Signature"),
    db: AsyncSession = Depends(get_async_db),
):
    """Webhook endpoint for payment events."""
    raw_payload = await request.body()
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    engine = WebhookEngine(db=db, secret=settings.PAYMENT_WEBHOOK_SECRET)
    result = await engine.process_event(
        provider="generic",
        payload=payload,
        signature=x_signature,
        raw_payload=raw_payload
    )
    return result


@router.post("/confirm")
async def confirm_payment(
    payload: dict,
    service: PaymentService = Depends(get_payment_service),
):
    """Confirm payment (Mock/Simulation)."""
    reference = payload.get("reference")
    if not reference:
        raise HTTPException(status_code=400, detail="Referência não fornecida")

    payment = await service.get_by_reference(reference)
    if not payment:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")

    await service.update_payment_status(payment.id, PaymentStatus.COMPLETED)
    return {"status": "confirmed", "reference": reference}
