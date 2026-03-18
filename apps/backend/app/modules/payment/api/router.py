"""Routers para API de Pagamentos."""
import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from ..application.dto.payment_schema import (
    CreatePaymentSchema,
    PaymentResponse,
    PaymentHistoryResponse,
)
from ..application.services.payment_service import PaymentService
from ..application.ports import (
    PaymentRepositoryPort,
    InvoiceRepositoryPort,
)
from ..domain.exceptions import (
    DuplicatePaymentError,
    InvoiceNotFoundError,
    InvalidInvoiceStateError,
    DomainValidationError,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/payment",
    tags=["payments"],
    responses={
        404: {"description": "Not found"},
        400: {"description": "Validation error"},
    },
)


# Dependency injection (será implementado na infrastructure)
async def get_payment_service() -> PaymentService:
    """Dependency para injetar PaymentService."""
    # Esta implementação será completada na fase de infraestrutura
    raise NotImplementedError("PaymentService dependency não configurado")


@router.post(
    "/register",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new payment",
    responses={
        201: {"description": "Payment registered successfully"},
        400: {"description": "Invalid payment data"},
        409: {"description": "Duplicate payment (idempotency)"},
    },
)
async def register_payment(
    payment_data: CreatePaymentSchema,
    payment_service: PaymentService = Depends(get_payment_service),
) -> PaymentResponse:
    """
    Registar um novo pagamento.
    
    A idempotência é garantida via gateway_reference. Se o mesmo pagamento
    for enviado múltiplas vezes, recebe sempre a mesma resposta sem duplicação.
    
    Args:
        payment_data: Detalhes do pagamento
        payment_service: Serviço de pagamentos (injetado)
        
    Returns:
        PaymentResponse com pagamento registado
        
    Raises:
        DuplicatePaymentError: Se gateway_reference já existe
        InvoiceNotFoundError: Se fatura não existe
        InvalidInvoiceStateError: Se fatura não está pagável
    """
    try:
        payment = await payment_service.register_payment(payment_data)
        return PaymentResponse(
            id=payment.id,
            invoice_id=payment.invoice_id,
            citizen_id=payment.citizen_id,
            amount=payment.amount,
            currency=payment.currency,
            gateway_reference=payment.gateway_reference,
            payment_method=payment.payment_method,
            status=payment.status.value,
            created_at=payment.created_at.isoformat(),
            confirmed_at=payment.confirmed_at.isoformat()
            if payment.confirmed_at
            else None,
        )
    except DuplicatePaymentError as e:
        logger.warning(f"Tentativa de pagamento duplicado: {e.gateway_reference}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except InvoiceNotFoundError as e:
        logger.error(f"Fatura não encontrada: {e.invoice_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except InvalidInvoiceStateError as e:
        logger.error(f"Estado inválido da fatura: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except DomainValidationError as e:
        logger.error(f"Violação de regra de domínio: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/citizen/{citizen_id}/history",
    response_model=PaymentHistoryResponse,
    summary="Get payment history for a citizen",
)
async def get_payment_history(
    citizen_id: str,
    payment_service: PaymentService = Depends(get_payment_service),
) -> PaymentHistoryResponse:
    """
    Recuperar histórico de pagamentos de um cidadão.
    
    Args:
        citizen_id: ID do cidadão
        payment_service: Serviço de pagamentos
        
    Returns:
        PaymentHistoryResponse com lista completa de pagamentos
    """
    try:
        payments = await payment_service.get_payment_history(citizen_id)
        return PaymentHistoryResponse(
            total_count=len(payments),
            payments=[
                PaymentResponse(
                    id=p.id,
                    invoice_id=p.invoice_id,
                    citizen_id=p.citizen_id,
                    amount=p.amount,
                    currency=p.currency,
                    gateway_reference=p.gateway_reference,
                    payment_method=p.payment_method,
                    status=p.status.value,
                    created_at=p.created_at.isoformat(),
                    confirmed_at=p.confirmed_at.isoformat()
                    if p.confirmed_at
                    else None,
                )
                for p in payments
            ],
        )
    except Exception as e:
        logger.error(f"Erro ao recuperar histórico: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao recuperar histórico de pagamentos",
        )


@router.get(
    "/reference/{gateway_reference}",
    response_model=Optional[PaymentResponse],
    summary="Get payment by gateway reference",
)
async def get_payment_by_reference(
    gateway_reference: str,
    payment_service: PaymentService = Depends(get_payment_service),
) -> Optional[PaymentResponse]:
    """
    Buscar pagamento por referência de gateway (ideal para reconciliação).
    
    Args:
        gateway_reference: Referência do gateway de pagamento
        payment_service: Serviço de pagamentos
        
    Returns:
        PaymentResponse ou None se não encontrado
    """
    try:
        payment = await payment_service.get_payment_by_reference(gateway_reference)
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pagamento com referência '{gateway_reference}' não encontrado",
            )
        return PaymentResponse(
            id=payment.id,
            invoice_id=payment.invoice_id,
            citizen_id=payment.citizen_id,
            amount=payment.amount,
            currency=payment.currency,
            gateway_reference=payment.gateway_reference,
            payment_method=payment.payment_method,
            status=payment.status.value,
            created_at=payment.created_at.isoformat(),
            confirmed_at=payment.confirmed_at.isoformat()
            if payment.confirmed_at
            else None,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar pagamento: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar pagamento",
        )


@router.get(
    "/invoice/{invoice_id}/payments",
    response_model=List[PaymentResponse],
    summary="List payments by invoice",
)
async def list_payments_by_invoice(
    invoice_id: str,
    payment_service: PaymentService = Depends(get_payment_service),
) -> List[PaymentResponse]:
    """
    Listar todos os pagamentos associados a uma fatura.
    
    Args:
        invoice_id: ID da fatura
        payment_service: Serviço de pagamentos
        
    Returns:
        Lista de PaymentResponse
    """
    try:
        payments = await payment_service.list_payments_by_invoice(invoice_id)
        return [
            PaymentResponse(
                id=p.id,
                invoice_id=p.invoice_id,
                citizen_id=p.citizen_id,
                amount=p.amount,
                currency=p.currency,
                gateway_reference=p.gateway_reference,
                payment_method=p.payment_method,
                status=p.status.value,
                created_at=p.created_at.isoformat(),
                confirmed_at=p.confirmed_at.isoformat()
                if p.confirmed_at
                else None,
            )
            for p in payments
        ]
    except Exception as e:
        logger.error(f"Erro ao listar pagamentos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar pagamentos",
        )


__all__ = ["router", "get_payment_service"]
