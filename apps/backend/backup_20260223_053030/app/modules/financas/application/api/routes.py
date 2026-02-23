import logging
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.api.deps import get_current_user
from modules.identity.models.user import User
from app.modules.financas.application.services.invoice_service import InvoiceService
from app.modules.financas.application.services.payment_service import PaymentService
from app.modules.financas.application.api.deps import get_invoice_service, get_payment_service
from app.modules.financas.schemas.invoice_schema import CreateInvoiceSchema, InvoiceResponse
from app.modules.financas.schemas.payment_schema import CreatePaymentSchema, PaymentResponse
from app.modules.financas.exceptions import (
    FinanceError, 
    InvoiceNotFoundError, 
    InvalidInvoiceStateError,
    DuplicatePaymentError
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/financas", tags=["Finanças"])


# --- INVOICES ---

@router.post(
    "/invoices", 
    response_model=InvoiceResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Emitir nova fatura"
)
async def create_invoice(
    data: CreateInvoiceSchema,
    current_user: User = Depends(get_current_user),
    service: InvoiceService = Depends(get_invoice_service),
):
    """
    Emite uma nova fatura oficial para um serviço público.
    
    Validações:
    - Cidadão deve estar ATIVO no FUC
    - Montante > 0 (validado no domínio)
    - Códigos orçamentais válidos
    """
    try:
        logger.info(f"Criando fatura para cidadão: {data.citizen_id}")
        invoice = await service.create_invoice(data)
        return invoice
    except FinanceError as e:
        logger.warning(f"Erro financeiro na criação: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Erro inesperado ao criar fatura: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno ao processar fatura"
        )


@router.get(
    "/invoices/{invoice_id}", 
    response_model=InvoiceResponse,
    summary="Consultar fatura por ID"
)
async def get_invoice(
    invoice_id: str,
    current_user: User = Depends(get_current_user),
    service: InvoiceService = Depends(get_invoice_service),
):
    """
    Recupera detalhes de uma fatura.
    
    Segurança: Cidadãos só acedem às suas próprias faturas.
    """
    try:
        invoice = await service.get_invoice(invoice_id)
    except InvoiceNotFoundError as e:
        logger.warning(f"Fatura não encontrada: {invoice_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao recuperar fatura: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno")
    
    # Autorização: Validate ownership (outside try-except to avoid 500 on 403)
    if current_user.role == "citizen" and invoice.citizen_id != current_user.citizen_id:
        logger.warning(f"Acesso negado: cidadão {current_user.citizen_id} tentou acessar fatura de {invoice.citizen_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Acesso negado a esta fatura"
        )
        
    return invoice


@router.get(
    "/invoices/citizen/{citizen_id}", 
    response_model=List[InvoiceResponse],
    summary="Listar faturas do cidadão"
)
async def list_citizen_invoices(
    citizen_id: str,
    current_user: User = Depends(get_current_user),
    service: InvoiceService = Depends(get_invoice_service),
):
    """
    Retorna histórico de faturas de um cidadão.
    
    Segurança: Cidadãos só veem suas próprias faturas.
    """
    # Authorization check
    if current_user.role == "citizen" and citizen_id != current_user.citizen_id:
        logger.warning(f"Acesso negado: cidadão tentou listar faturas de outro")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado")
    
    try:
        invoices = await service.list_citizen_invoices(citizen_id)
        return invoices
    except Exception as e:
        logger.error(f"Erro ao listar faturas: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno")


@router.post(
    "/invoices/{invoice_id}/cancel", 
    response_model=InvoiceResponse,
    summary="Cancelar fatura"
)
async def cancel_invoice(
    invoice_id: str,
    reason: str = "Cancelamento solicitado",
    current_user: User = Depends(get_current_user),
    service: InvoiceService = Depends(get_invoice_service),
):
    """
    Cancela uma fatura pendente.
    
    REGRA: Apenas PENDING ou OVERDUE podem ser canceladas.
    PAID e CANCELLED são estados finais.
    """
    try:
        invoice = await service.get_invoice(invoice_id)
        
        # Authorization: Citizens can only cancel own invoices
        if current_user.role == "citizen" and invoice.citizen_id != current_user.citizen_id:
            logger.warning(f"Tentativa de cancelamento não autorizado")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão insuficiente")

        result = await service.cancel_invoice(invoice_id, reason)
        logger.info(f"Fatura {invoice_id} cancelada: {reason}")
        return result
        
    except (InvoiceNotFoundError, InvalidInvoiceStateError) as e:
        logger.warning(f"Erro ao cancelar fatura: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao cancelar fatura: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno")


@router.get(
    "/invoices/citizen/{citizen_id}/pending",
    response_model=List[InvoiceResponse],
    summary="Listar faturas pendentes"
)
async def list_pending_invoices(
    citizen_id: str,
    current_user: User = Depends(get_current_user),
    service: InvoiceService = Depends(get_invoice_service),
):
    """
    Lista faturas PENDING ou OVERDUE para um cidadão.
    """
    # Authorization
    if current_user.role == "citizen" and citizen_id != current_user.citizen_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado")
    
    try:
        invoices = await service.get_pending_by_citizen(citizen_id)
        return invoices
    except Exception as e:
        logger.error(f"Erro ao listar faturas pendentes: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno")


# --- PAYMENTS ---

@router.post(
    "/payments", 
    response_model=PaymentResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Registar pagamento"
)
async def register_payment(
    data: CreatePaymentSchema,
    current_user: User = Depends(get_current_user),
    service: PaymentService = Depends(get_payment_service),
):
    """
    Registra um pagamento e liquida a fatura correspondente.
    
    SISTEMA DE IDEMPOTÊNCIA:
    - gateway_reference previne pagamentos duplicados
    - Mesmo erro 409 se gateway_reference já existe
    
    REGRAS FINANCEIRAS:
    - Fatura must exist
    - Fatura must be PENDING ou OVERDUE
    - Montante deve corresponder ao da fatura
    """
    try:
        logger.info(f"Registando pagamento: ref={data.gateway_reference}")
        result = await service.register_payment(data)
        logger.info(f"Pagamento {result.id} processado com sucesso")
        return result
        
    except DuplicatePaymentError as e:
        logger.warning(f"Tentativa de pagamento duplicado: {data.gateway_reference}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except FinanceError as e:
        logger.warning(f"Erro financeiro no pagamento: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao processar pagamento: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Falha técnica no processamento"
        )


@router.get(
    "/payments/citizen/{citizen_id}", 
    response_model=List[PaymentResponse],
    summary="Histórico de pagamentos"
)
async def list_citizen_payments(
    citizen_id: str,
    current_user: User = Depends(get_current_user),
    service: PaymentService = Depends(get_payment_service),
):
    """
    Recupera todos os pagamentos realizados por um cidadão.
    
    Segurança: Cidadãos só veem seus próprios pagamentos.
    """
    # Authorization
    if current_user.role == "citizen" and citizen_id != current_user.citizen_id:
        logger.warning(f"Acesso negado ao histórico de pagamentos")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado")

    try:
        payments = await service.get_payment_history(citizen_id)
        return payments
    except Exception as e:
        logger.error(f"Erro ao recuperar histórico: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno")


@router.get(
    "/payments/gateway/{gateway_reference}",
    response_model=PaymentResponse,
    summary="Consultar pagamento por referência de gateway"
)
async def get_payment_by_gateway_ref(
    gateway_reference: str,
    current_user: User = Depends(get_current_user),
    service: PaymentService = Depends(get_payment_service),
):
    """
    Busca status de pagamento usando referência do gateway (reconciliação).
    
    Ideal para: Webhooks, consultas de status, reconciliação bancária.
    """
    try:
        payment = await service.get_payment_by_reference(gateway_reference)
        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pagamento não encontrado")
        
        # Authorization: Only allowed for admins or own payments
        if current_user.role == "citizen" and payment.citizen_id != current_user.citizen_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado")
            
        return payment
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar pagamento: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno")
