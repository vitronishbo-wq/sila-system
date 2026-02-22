"""Payment router - API endpoints completo com CRUD, transações, reembolsos, webhooks e auditoria."""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.session import get_db
from ..crud import PaymentCRUD, get_payment_crud
from ..models.payment import Payment
from ..models.transaction import PaymentTransaction
from ..models.refund import Refund
from ..models.enums import (
    PaymentStatus,
    PaymentMethod,
    TransactionStatus,
    TransactionType,
)
from ..schemas.payment import (
    PaymentCreate,
    PaymentResponse,
    PaymentUpdate,
    RefundCreate,
    RefundResponse,
    TransactionResponse,
    PaymentFilter,
)
from ..services.payment_service import PaymentService

router = APIRouter(tags=["Payments"])


# ==========================================
# HEALTH CHECK ENDPOINTS
# ==========================================


@router.get("/ping")
async def ping():
    """Health check do módulo de pagamento."""
    return {
        "status": "payment ok",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "payment-module",
    }


@router.get("/status")
async def status_check():
    """Status detalhado do módulo de pagamento."""
    return {
        "status": "healthy",
        "service": "payment",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "create": "POST /api/v1/payment/",
            "list": "GET /api/v1/payment/",
            "get": "GET /api/v1/payment/{id}",
            "update": "PUT /api/v1/payment/{id}",
            "delete": "DELETE /api/v1/payment/{id}",
            "by_reference": "GET /api/v1/payment/reference/{reference}",
            "create_transaction": "POST /api/v1/payment/{id}/transaction",
            "create_refund": "POST /api/v1/payment/{id}/refund",
            "get_transaction": "GET /api/v1/payment/transaction/{transaction_id}",
            "get_refund": "GET /api/v1/payment/refund/{refund_id}",
            "statistics": "GET /api/v1/payment/statistics",
            "audit_log": "GET /api/v1/payment/audit-log",
            "webhook_register": "POST /api/v1/payment/webhook/register",
            "webhook_test": "POST /api/v1/payment/webhook/test",
            "receipt": "GET /api/v1/payment/{id}/receipt",
        },
    }


# ==========================================
# PAYMENT CRUD ENDPOINTS
# ==========================================


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment: PaymentCreate,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = 1,  # TODO: substituir por autenticação real
):
    """
    Criar um novo pagamento.

    - **amount**: Valor do pagamento (obrigatório, > 0)
    - **currency**: Moeda (padrão: AOA)
    - **method**: Método de pagamento (BNA, UNITEL_MONEY, M_PESA, etc.)
    - **description**: Descrição do pagamento
    - **reference**: Referência externa (opcional)
    """
    try:
        crud = PaymentCRUD(db)
        db_obj = await crud.create(payment, created_by=current_user_id)
        return PaymentResponse.model_validate(db_obj)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar pagamento: {str(e)}",
        )


@router.get("/", response_model=List[PaymentResponse])
async def list_payments(
    status_filter: Optional[str] = Query(None, alias="status"),
    method: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    min_amount: Optional[float] = Query(None),
    max_amount: Optional[float] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    crud: PaymentCRUD = Depends(get_payment_crud),
):
    """
    Listar pagamentos com filtros opcionais.

    - **status**: Filtrar por status (pending, processing, completed, failed, etc.)
    - **method**: Filtrar por método de pagamento
    - **date_from**: Data inicial (YYYY-MM-DD)
    - **date_to**: Data final (YYYY-MM-DD)
    - **min_amount**: Valor mínimo
    - **max_amount**: Valor máximo
    - **skip**: Número de registros a pular
    - **limit**: Número máximo de registros
    """
    filters = PaymentFilter(
        status=status_filter,
        method=method,
        date_from=date_from,
        date_to=date_to,
        min_amount=min_amount,
        max_amount=max_amount,
    )
    db_objs = await crud.get_filtered(filters, skip=skip, limit=limit)
    return [PaymentResponse.model_validate(obj) for obj in db_objs]


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
    crud: PaymentCRUD = Depends(get_payment_crud),
):
    """Recuperar um pagamento pelo ID."""
    payment = await crud.get(payment_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pagamento não encontrado"
        )
    return PaymentResponse.model_validate(payment)


@router.get("/reference/{reference}", response_model=PaymentResponse)
async def get_payment_by_reference(
    reference: str,
    db: AsyncSession = Depends(get_db),
    crud: PaymentCRUD = Depends(get_payment_crud),
):
    """Recuperar um pagamento pela referência."""
    payment = await crud.get_by_reference(reference)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pagamento não encontrado com essa referência",
        )
    return PaymentResponse.model_validate(payment)


@router.put("/{payment_id}", response_model=PaymentResponse)
async def update_payment(
    payment_id: int,
    update_data: PaymentUpdate,
    db: AsyncSession = Depends(get_db),
    crud: PaymentCRUD = Depends(get_payment_crud),
):
    """Atualizar um pagamento existente."""
    payment = await crud.get(payment_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pagamento não encontrado"
        )

    # Buscar objeto do banco para atualizar
    from sqlalchemy import select

    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    db_payment = result.scalar_one_or_none()

    updated = await crud.update(db_payment, update_data)
    return PaymentResponse.model_validate(updated)


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
    crud: PaymentCRUD = Depends(get_payment_crud),
):
    """Deletar um pagamento."""
    success = await crud.delete(payment_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pagamento não encontrado"
        )
    return None


# ==========================================
# TRANSACTION ENDPOINTS
# ==========================================


@router.post(
    "/{payment_id}/transaction",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction(
    payment_id: int,
    transaction_type: TransactionType = Query(..., description="Tipo de transação"),
    amount: Optional[float] = Query(
        None, description="Valor da transação (se diferente do pagamento)"
    ),
    db: AsyncSession = Depends(get_db),
    service: PaymentService = Depends(lambda db=Depends(get_db): PaymentService(db)),
):
    """
    Criar uma transação para um pagamento.

    - **payment_id**: ID do pagamento
    - **transaction_type**: Tipo de transação (payment, refund, adjustment, fee)
    - **amount**: Valor (opcional, usa valor do pagamento se não informado)
    """
    try:
        transaction = await service.create_transaction(
            payment_id=payment_id, transaction_type=transaction_type, amount=amount
        )
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Falha ao criar transação",
            )
        return TransactionResponse.model_validate(transaction)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar transação: {str(e)}",
        )


@router.get("/transaction/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Recuperar uma transação pelo ID."""
    from sqlalchemy import select

    result = await db.execute(
        select(PaymentTransaction).where(PaymentTransaction.id == transaction_id)
    )
    transaction = result.scalar_one_or_none()
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transação não encontrada"
        )
    return TransactionResponse.model_validate(transaction)


@router.get("/{payment_id}/transactions", response_model=List[TransactionResponse])
async def list_payment_transactions(
    payment_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    """Listar todas as transações de um pagamento."""
    from sqlalchemy import select

    result = await db.execute(
        select(PaymentTransaction)
        .where(PaymentTransaction.payment_id == payment_id)
        .offset(skip)
        .limit(limit)
        .order_by(PaymentTransaction.created_at.desc())
    )
    transactions = result.scalars().all()
    return [TransactionResponse.model_validate(t) for t in transactions]


# ==========================================
# REFUND ENDPOINTS
# ==========================================


@router.post(
    "/{payment_id}/refund",
    response_model=RefundResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_refund(
    payment_id: int,
    refund_data: RefundCreate,
    db: AsyncSession = Depends(get_db),
    service: PaymentService = Depends(lambda db=Depends(get_db): PaymentService(db)),
):
    """
    Criar um reembolso para um pagamento.

    - **payment_id**: ID do pagamento
    - **amount**: Valor do reembolso (opcional, usa valor total se não informado)
    - **reason**: Motivo do reembolso
    - **metadata**: Dados adicionais do reembolso
    """
    try:
        refund = await service.create_refund(payment_id, refund_data, user_id=1)
        if not refund:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Falha ao criar reembolso",
            )
        return RefundResponse.model_validate(refund)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar reembolso: {str(e)}",
        )


@router.get("/refund/{refund_id}", response_model=RefundResponse)
async def get_refund(
    refund_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Recuperar um reembolso pelo ID."""
    from sqlalchemy import select

    result = await db.execute(select(Refund).where(Refund.id == refund_id))
    refund = result.scalar_one_or_none()
    if not refund:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reembolso não encontrado"
        )
    return RefundResponse.model_validate(refund)


@router.get("/{payment_id}/refunds", response_model=List[RefundResponse])
async def list_payment_refunds(
    payment_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    """Listar todos os reembolsos de um pagamento."""
    from sqlalchemy import select

    result = await db.execute(
        select(Refund)
        .where(Refund.payment_id == payment_id)
        .offset(skip)
        .limit(limit)
        .order_by(Refund.created_at.desc())
    )
    refunds = result.scalars().all()
    return [RefundResponse.model_validate(r) for r in refunds]


# ==========================================
# STATISTICS & ANALYTICS ENDPOINTS
# ==========================================


@router.get("/statistics", tags=["analytics"])
async def get_payment_statistics(
    db: AsyncSession = Depends(get_db),
    crud: PaymentCRUD = Depends(get_payment_crud),
):
    """
    Obter estatísticas gerais de pagamentos.

    Retorna:
    - Total de pagamentos
    - Valor total processado
    - Pagamentos completados
    - Valor completado
    - Pagamentos pendentes
    """
    stats = await crud.get_statistics()
    return {"timestamp": datetime.utcnow().isoformat(), "statistics": stats}


@router.get("/{payment_id}/summary", tags=["analytics"])
async def get_payment_summary(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
    service: PaymentService = Depends(lambda db=Depends(get_db): PaymentService(db)),
):
    """Obter resumo completo de um pagamento com transações e reembolsos."""
    try:
        summary = await service.get_payment_summary(payment_id)
        if not summary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pagamento não encontrado"
            )
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao obter resumo: {str(e)}",
        )


# ==========================================
# AUDIT LOG ENDPOINTS
# ==========================================


@router.get("/audit-log", tags=["audit"])
async def get_audit_log(
    payment_id: Optional[int] = Query(None),
    action: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    """
    Obter log de auditoria de pagamentos.

    - **payment_id**: Filtrar por ID de pagamento
    - **action**: Filtrar por ação (create, update, refund, etc.)
    - **skip**: Número de registros a pular
    - **limit**: Número máximo de registros
    """
    from sqlalchemy import select
    from ..models.audit_log import PaymentAuditLog

    query = select(PaymentAuditLog)

    if payment_id:
        query = query.where(PaymentAuditLog.payment_id == payment_id)
    if action:
        query = query.where(PaymentAuditLog.action == action)

    result = await db.execute(
        query.offset(skip).limit(limit).order_by(PaymentAuditLog.created_at.desc())
    )
    logs = result.scalars().all()

    return {
        "total": len(logs),
        "logs": [
            {
                "id": log.id,
                "payment_id": log.payment_id,
                "action": log.action,
                "user_id": log.user_id,
                "details": log.details,
                "created_at": log.created_at.isoformat(),
            }
            for log in logs
        ],
    }


# ==========================================
# WEBHOOK ENDPOINTS
# ==========================================


@router.post("/webhook/register", tags=["webhooks"])
async def register_webhook(
    url: str = Query(..., description="URL do webhook"),
    events: List[str] = Query(..., description="Eventos para disparar o webhook"),
    db: AsyncSession = Depends(get_db),
):
    """
    Registrar um webhook para eventos de pagamento.

    Eventos disponíveis:
    - payment.created
    - payment.completed
    - payment.failed
    - payment.refunded
    - transaction.created
    - transaction.completed
    """
    try:
        from ..models.webhook import PaymentWebhook

        webhook = PaymentWebhook(url=url, events=events, active=True)
        db.add(webhook)
        await db.commit()
        await db.refresh(webhook)

        return {
            "id": webhook.id,
            "url": webhook.url,
            "events": webhook.events,
            "active": webhook.active,
            "created_at": webhook.created_at.isoformat(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao registrar webhook: {str(e)}",
        )


@router.post("/webhook/test", tags=["webhooks"])
async def test_webhook(
    webhook_id: int = Query(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: AsyncSession = Depends(get_db),
    service: PaymentService = Depends(lambda db=Depends(get_db): PaymentService(db)),
):
    """Testar um webhook enviando um evento de teste."""
    try:
        result = await service.test_webhook(webhook_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Webhook não encontrado"
            )

        return {
            "status": "test_sent",
            "webhook_id": webhook_id,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao testar webhook: {str(e)}",
        )


# ==========================================
# RECEIPT ENDPOINTS
# ==========================================


@router.get("/{payment_id}/receipt", tags=["receipts"])
async def get_payment_receipt(
    payment_id: int,
    format: str = Query("pdf", regex="^(pdf|json|html)$"),
    db: AsyncSession = Depends(get_db),
    service: PaymentService = Depends(lambda db=Depends(get_db): PaymentService(db)),
):
    """
    Obter recibo de um pagamento.

    - **format**: Formato do recibo (pdf, json, html)
    """
    try:
        receipt = await service.generate_receipt(payment_id, format=format)
        if not receipt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pagamento não encontrado"
            )

        if format == "pdf":
            from fastapi.responses import FileResponse

            return FileResponse(receipt, media_type="application/pdf")

        return receipt
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao gerar recibo: {str(e)}",
        )
