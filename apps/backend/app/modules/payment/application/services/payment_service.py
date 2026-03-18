"""Serviço de Domínio para Gestão de Pagamentos com Reconciliação Bancária."""
import uuid
import logging
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from apps.backend.app.core.observability import trace

from ...domain.models import Payment, Invoice
from ...domain.enums import PaymentStatus, InvoiceStatus
from ...domain.exceptions import (
    DuplicatePaymentError,
    InvoiceNotFoundError,
    InvalidInvoiceStateError,
    DomainValidationError,
)
from ..ports import (
    PaymentRepositoryPort,
    InvoiceRepositoryPort,
    EducacaoServicePort,
    JuventudeServicePort,
    EmpregoServicePort,
    SaudeServicePort,
    AssistenciaSocialServicePort,
    ServiceRequestsServicePort,
)
from ..dto.payment_schema import CreatePaymentSchema

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
        invoice_repository: InvoiceRepositoryPort,
        educacao_service: Optional[EducacaoServicePort] = None,
        juventude_service: Optional[JuventudeServicePort] = None,
        emprego_service: Optional[EmpregoServicePort] = None,
        saude_service: Optional[SaudeServicePort] = None,
        assistencia_social_service: Optional[AssistenciaSocialServicePort] = None,
        service_requests_service: Optional[ServiceRequestsServicePort] = None,
    ):
        self.payment_repo = payment_repository
        self.invoice_repo = invoice_repository
        self._module_adapters = {
            "educacao": educacao_service,
            "juventude": juventude_service,
            "emprego": emprego_service,
            "saude": saude_service,
            "assistencia_social": assistencia_social_service,
            "service_requests": service_requests_service,
        }

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

        Exceções esperadas:
        - DuplicatePaymentError: gateway_reference já existe
        - InvoiceNotFoundError: Fatura não encontrada
        - InvalidInvoiceStateError: Fatura não está PENDING/OVERDUE
        """
        logger.info(
            f"Registando pagamento para fatura: {data.invoice_id} "
            f"(ref: {data.gateway_reference})"
        )

        # Check idempotência
        if await self.payment_repo.exists_by_gateway_ref(data.gateway_reference):
            logger.warning(
                f"Pagamento duplicado interceptado: {data.gateway_reference}"
            )
            raise DuplicatePaymentError(data.gateway_reference)

        # Valida fatura
        invoice = await self.invoice_repo.get_by_id(data.invoice_id)
        if not invoice:
            logger.error(f"Fatura não encontrada: {data.invoice_id}")
            raise InvoiceNotFoundError(data.invoice_id)

        # Verifica consistência de valores
        if round(float(data.amount), 2) != round(float(invoice.amount), 2):
            raise DomainValidationError(
                "Montante do pagamento divergente do valor da fatura"
            )

        # Verifica estado da fatura
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

        # Cria Payment
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
            confirmed_at=datetime.now(timezone.utc),
        )

        try:
            # Atualiza estado da fatura
            invoice.change_status(
                InvoiceStatus.PAID,
                reason=f"Liquidado via {data.payment_method} - "
                       f"Ref: {data.gateway_reference}"
            )

            # Persistência atômica
            new_payment = await self.payment_repo.create(payment)
            await self.invoice_repo.save(invoice)

            # Notifica módulo de origem
            await self._notify_origin_module(invoice, new_payment)

            logger.info(
                f"Pagamento {new_payment.id} processado. "
                f"Fatura {invoice.reference} marcada como PAGA"
            )
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
    async def get_payment_by_reference(
        self, reference: str
    ) -> Optional[Payment]:
        """Busca pagamento por referência (ideal para reconciliação)."""
        return await self.payment_repo.get_by_gateway_ref(reference)

    @trace()
    async def list_payments_by_invoice(self, invoice_id: str) -> List[Payment]:
        """Lista todos os pagamentos associados a uma fatura."""
        logger.info(f"Recuperando pagamentos da fatura: {invoice_id}")
        return await self.payment_repo.list_by_invoice(invoice_id)

    async def _notify_origin_module(self, invoice: Invoice, payment: Payment) -> None:
        """Notifica módulo de origem sobre pagamento processado."""
        module_name = self._resolve_module_name(invoice.service_code)
        if module_name is None:
            return

        adapter = self._module_adapters.get(module_name)
        if adapter is None:
            return

        reference_id = self._parse_request_reference(invoice.request_id)
        if reference_id is None:
            logger.info(
                "Callback financeiro ignorado por ausência de referência UUID",
                extra={
                    "invoice_id": invoice.id,
                    "service_code": invoice.service_code,
                },
            )
            return

        callback_name = {
            "educacao": "registrar_pagamento_propina",
            "juventude": "registrar_pagamento_bolsa",
            "emprego": "registrar_pagamento_salario",
            "saude": "registrar_pagamento_servico",
            "assistencia_social": "registrar_pagamento_beneficio",
            "service_requests": "registrar_pagamento_taxa",
        }.get(module_name)

        if callback_name is None:
            return

        callback = getattr(adapter, callback_name, None)
        if callback is None:
            return

        try:
            await callback(reference_id, payment.id, float(payment.amount))
        except Exception as exc:
            logger.warning(
                "Falha ao notificar módulo de origem do pagamento",
                extra={
                    "invoice_id": invoice.id,
                    "module": module_name,
                    "error": str(exc),
                },
            )

    @staticmethod
    def _resolve_module_name(service_code: Optional[str]) -> Optional[str]:
        """Resolve nome do módulo baseado no código de serviço."""
        code = (service_code or "").upper()
        prefix_map = {
            "EDU_": "educacao",
            "JUV_": "juventude",
            "EMP_": "emprego",
            "SAU_": "saude",
            "ASS_": "assistencia_social",
            "SRV_": "service_requests",
            "REQ_": "service_requests",
        }
        for prefix, module_name in prefix_map.items():
            if code.startswith(prefix):
                return module_name
        return None

    @staticmethod
    def _parse_request_reference(request_id: Optional[str]) -> Optional[UUID]:
        """Parse de UUID a partir de referência de pedido."""
        if not request_id:
            return None
        try:
            return UUID(str(request_id))
        except (TypeError, ValueError):
            return None

        return result.scalars().first()

    async def create_payment(self, payment_data: PaymentCreate, user_id: int):
        reference = await self._generate_reference('PAY')
        payment = Payment(amount=float(payment_data.amount), currency=payment_data.currency, method=payment_data.method, status=PaymentStatus.PENDING, reference=reference, description=payment_data.description, metadata_=payment_data.metadata)
        transaction = PaymentTransaction(payment_id=payment.id, amount=float(payment_data.amount), currency=payment_data.currency, type=TransactionType.PAYMENT, status=TransactionStatus.PENDING, reference=reference, metadata_={'user_id': user_id})
        self.db.add(payment)
        self.db.add(transaction)
        await self.db.commit()
        if hasattr(self.db, 'refresh'):
            await self.db.refresh(payment)
        return payment

    async def get_payment(self, payment_id: int):
        result = await self.db.execute(('payment', payment_id))
        return result.scalars().first()

    async def get_by_reference(self, reference: str):
        result = await self.db.execute(('payment_reference', reference))
        return result.scalars().first()

    async def update_status(self, payment_id: int, status: PaymentStatus):
        return await self.update_payment_status(payment_id=payment_id, status=status)

    async def update_payment_status(self, payment_id: int, status: PaymentStatus, provider_reference: str | None=None):
        payment = await self.get_payment(payment_id)
        if not payment:
            return None
        current_status = PaymentStatus(payment.status)
        if not self._is_valid_status_transition(current_status, status):
            raise ValueError('Invalid status transition')
        payment.status = status
        transaction = await self._get_latest_transaction(payment_id)
        if transaction:
            if status in {PaymentStatus.COMPLETED, PaymentStatus.REFUNDED}:
                transaction.status = TransactionStatus.COMPLETED
            elif status in {PaymentStatus.CANCELLED, PaymentStatus.FAILED}:
                transaction.status = TransactionStatus.FAILED
            else:
                transaction.status = TransactionStatus.PENDING
            if provider_reference:
                transaction.provider_reference = provider_reference
        await self.db.commit()
        return payment

    async def create_refund(self, payment_id: int, refund_data: RefundCreate, user_id: int) -> RefundResponse:
        payment = await self.get_payment(payment_id)
        if not payment:
            return None
        if PaymentStatus(payment.status) != PaymentStatus.COMPLETED:
            raise ValueError('Can only refund completed payments')
        payment_amount = Decimal(str(payment.amount))
        refund_amount = Decimal(str(refund_data.amount)) if refund_data.amount is not None else payment_amount
        if refund_amount > payment_amount:
            raise ValueError('Refund amount cannot exceed payment amount')
        refund_reference = await self._generate_reference('RFD')
        transaction = PaymentTransaction(payment_id=payment.id, amount=float(refund_amount), currency=getattr(payment, 'currency', 'AOA'), type=TransactionType.REFUND, status=TransactionStatus.PENDING, reference=refund_reference, metadata_={'user_id': user_id, 'reason': refund_data.reason})
        self.db.add(transaction)
        payment.status = PaymentStatus.REFUNDED if refund_amount == payment_amount else PaymentStatus.PARTIALLY_REFUNDED
        await self.db.commit()
        return RefundResponse(amount=float(refund_amount), status=TransactionStatus.PENDING, reference=refund_reference)

    async def delete_payment(self, payment_id: int, user_id: int) -> bool:
        payment = await self.get_payment(payment_id)
        if not payment:
            return False
        delete_result = self.db.delete(payment)
        if inspect.isawaitable(delete_result):
            await delete_result
        await self.db.commit()
        return True