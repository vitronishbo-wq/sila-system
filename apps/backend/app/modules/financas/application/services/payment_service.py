from app.core.observability import trace
import uuid
import logging
from datetime import datetime, timezone
from typing import List, Optional

from app.modules.financas.domain.models.payment import Payment
from app.modules.financas.domain.models.enums import PaymentStatus, InvoiceStatus
from app.modules.financas.application.ports.payment_repository_port import PaymentRepositoryPort
from app.modules.financas.application.ports.invoice_repository_port import InvoiceRepositoryPort
from app.modules.financas.api.schemas.payment_schema import CreatePaymentSchema
from app.modules.financas.exceptions import (
    DuplicatePaymentError, 
    InvoiceNotFoundError, 
    InvalidInvoiceStateError,
    DomainValidationError
)

logger = logging.getLogger(__name__)


class PaymentService:
    """
    Serviço de Gestão de Pagamentos com Reconciliação Bancária.
    
    REGRAS FINANCEIRAS:
    1. IDEMPOTÊNCIA: gateway_reference garante não há pagamentos duplicados
    2. INTEGRIDADE: Fatura must exists + estar em PENDING/OVERDUE
    3. TRANSAÇÃO: Pagamento + Invoice update são atômicos
    4. AUDITORIA: Todos os estados capturados para compliance
    
    Padrão de Inicialização:
    - payment_repository: Gerencia persistência de Payment
    - invoice_repository: Gerencia persistência de Invoice (reconciliação)
    """
    
    def __init__(
        self,
        payment_repository: PaymentRepositoryPort,
        invoice_repository: InvoiceRepositoryPort
    ):
        self.payment_repo = payment_repository
        self.invoice_repo = invoice_repository

    @trace()
    async def register_payment(self, data: CreatePaymentSchema) -> Payment:
        """
        Processa um pagamento com IDEMPOTÊNCIA garantida.
        
        Sequência:
        1. Check idempotência (gateway_reference)
        2. Valida fatura (exists + estado)
        3. Cria Payment (COMPLETED)
        4. Atualiza Invoice (PAID)
        5. Persistência atômica via flush
        
        Exeções esperadas:
        - DuplicatePaymentError: gateway_reference já existe
        - InvoiceNotFoundError: Fatura não encontrada
        - InvalidInvoiceStateError: Fatura não está PENDING/OVERDUE
        """
        logger.info(f"Registando pagamento para fatura: {data.invoice_id} "
                    f"(ref: {data.gateway_reference})")

        # 1. VERIFICAÇÃO IDEMPOTÊNCIA (Crítico para serviços financeiros)
        # Previne pagamentos duplicados da mesma transação bancária
        if await self.payment_repo.exists_by_gateway_ref(data.gateway_reference):
            logger.warning(f"Pagamento duplicado interceptado: {data.gateway_reference}")
            existing = await self.payment_repo.get_by_gateway_ref(data.gateway_reference)
            raise DuplicatePaymentError(data.gateway_reference)

        # 2. VALIDAÇÃO DA FATURA (Entidade Principal)
        invoice = await self.invoice_repo.get_by_id(data.invoice_id)
        if not invoice:
            logger.error(f"Fatura não encontrada: {data.invoice_id}")
            raise InvoiceNotFoundError(data.invoice_id)
        
        # 3. VERIFICAÇÃO DE ESTADO (Regra Financeira)
        # Apenas PENDING e OVERDUE podem ser pagos
        if invoice.status == InvoiceStatus.PAID:
            logger.error(f"Tentativa de pagar fatura já liquidada: {invoice.id}")
            raise InvalidInvoiceStateError(
                current_status=invoice.status.value,
                action="pagar novamente"
            )

        if invoice.status == InvoiceStatus.CANCELLED:
            logger.error(f"Tentativa de pagar fatura cancelada: {invoice.id}")
            raise InvalidInvoiceStateError(
                current_status=invoice.status.value,
                action="processar pagamento"
            )

        # 4. CRIAÇÃO DA ENTIDADE PAYMENT (Domínio)
        payment = Payment(
            id=str(uuid.uuid4()),
            invoice_id=data.invoice_id,
            citizen_id=data.citizen_id,
            amount=data.amount,
            currency=data.currency,
            gateway_reference=data.gateway_reference,
            payment_method=data.payment_method,
            status=PaymentStatus.COMPLETED,
            created_at=datetime.now(timezone.utc),
            confirmed_at=datetime.now(timezone.utc)
        )

        try:
            # 5. RECONCILIAÇÃO (Atualiza Invoice para PAID)
            invoice.change_status(
                InvoiceStatus.PAID, 
                reason=f"Liquidado via {data.payment_method} - Ref: {data.gateway_reference}"
            )

            # 6. PERSISTÊNCIA ATÔMICA
            # Ambas operações usam flush() para garantir atomicidade
            new_payment = await self.payment_repo.create(payment)
            await self.invoice_repo.save(invoice)
            
            logger.info(f"Pagamento {new_payment.id} processado. "
                       f"Fatura {invoice.reference} marcada como PAGA")
            return new_payment

        except DomainValidationError as e:
            logger.error(f"Violação de regra: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Falha ao processar pagamento: {str(e)}")
            raise

    @trace()
    async def get_payment_history(self, citizen_id: str) -> List[Payment]:
        """Recupera histórico de pagamentos do cidadão."""
        logger.info(f"Recuperando histórico de pagamentos: {citizen_id}")
        return await self.payment_repo.get_by_citizen(citizen_id)

    @trace()
    async def get_payment_by_reference(self, reference: str) -> Optional[Payment]:
        """Busca pagamento por referência (ideal para reconciliação)."""
        return await self.payment_repo.get_by_gateway_ref(reference)

    @trace()
    async def list_payments_by_invoice(self, invoice_id: str) -> List[Payment]:
        """Lista todos os pagamentos associados a uma fatura."""
        logger.info(f"Recuperando pagamentos da fatura: {invoice_id}")
        return await self.payment_repo.list_by_invoice(invoice_id)
