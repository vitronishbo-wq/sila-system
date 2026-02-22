"""Payment Endpoints

Este módulo define os endpoints da API para operações de pagamento no sistema SILA.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.session import get_db
from modules.payment.crud import PaymentCRUD, get_payment_crud
from modules.payment.models.payment import Payment
from modules.payment.models.transaction import PaymentTransaction
from modules.payment.schemas.payment import (
    PaymentCreate,
    PaymentResponse,
    PaymentUpdate,
    RefundCreate,
    RefundResponse,
    TransactionResponse,
    PaymentFilter,
)

router = APIRouter(tags=["payments"])


# ---------------------------
# Health Check Endpoints
# ---------------------------


@router.get("/ping")
async def ping():
    """Health check simples do módulo de pagamento."""
    return {"message": "Payment service is alive!"}


@router.get("/status")
async def status():
    """Status geral do módulo de pagamento."""
    from datetime import datetime

    return {
        "status": "healthy",
        "service": "payment",
        "timestamp": datetime.utcnow().isoformat(),
    }


# ---------------------------
# Payment Endpoints
# ---------------------------


@router.post("/", response_model=PaymentResponse, status_code=201)
async def create_payment(
    payment: PaymentCreate,
    db: AsyncSession = Depends(get_db),
    crud: PaymentCRUD = Depends(get_payment_crud),
    current_user_id: int = 1,  # substituir por autenticação real
):
    """Criar um novo pagamento."""
    db_obj = await crud.create(payment, created_by=current_user_id)
    return PaymentResponse.model_validate(db_obj)


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Recuperar um pagamento pelo ID."""
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    payment = result.scalars().first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return PaymentResponse.model_validate(payment)


@router.get("/", response_model=List[PaymentResponse])
async def list_payments(
    status: Optional[str] = Query(None),
    method: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    min_amount: Optional[float] = Query(None),
    max_amount: Optional[float] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    crud: PaymentCRUD = Depends(get_payment_crud),
):
    """Listar pagamentos com filtros opcionais."""
    filters = PaymentFilter(
        status=status,
        method=method,
        date_from=date_from,
        date_to=date_to,
        min_amount=min_amount,
        max_amount=max_amount,
    )
    db_objs = await crud.get_filtered(filters, skip=skip, limit=limit)
    return [PaymentResponse.model_validate(obj) for obj in db_objs]


@router.put("/{payment_id}", response_model=PaymentResponse)
async def update_payment(
    payment_id: int,
    update_data: PaymentUpdate,
    db: AsyncSession = Depends(get_db),
    crud: PaymentCRUD = Depends(get_payment_crud),
):
    """Atualizar um pagamento existente."""
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    payment = result.scalars().first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    updated = await crud.update(payment, update_data)
    return PaymentResponse.model_validate(updated)


# ---------------------------
# Refund Endpoints
# ---------------------------


@router.post("/{payment_id}/refund", response_model=RefundResponse, status_code=201)
async def create_refund(
    payment_id: int,
    refund_data: RefundCreate,
    db: AsyncSession = Depends(get_db),
    # user_id temporário, substituir por autenticação real
):
    """Criar um reembolso para um pagamento."""
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    payment = result.scalars().first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    from modules.payment.services.payment_service import PaymentService

    service = PaymentService(db)
    refund = await service.create_refund(payment_id, refund_data, user_id=1)
    if not refund:
        raise HTTPException(status_code=400, detail="Failed to create refund")
    return RefundResponse.model_validate(refund)


# ---------------------------
# Transaction Endpoints
# ---------------------------


@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Recuperar uma transação pelo ID."""
    result = await db.execute(
        select(PaymentTransaction).where(PaymentTransaction.id == transaction_id)
    )
    transaction = result.scalars().first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return TransactionResponse.model_validate(transaction)
