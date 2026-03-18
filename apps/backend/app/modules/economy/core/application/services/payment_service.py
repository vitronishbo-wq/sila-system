from apps.backend.app.core.observability import trace
import uuid
import logging
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID
from ....domain.models.payment import Payment
from ....domain.models.enums import PaymentStatus, InvoiceStatus
from ....domain.ports.payment_repository_port import PaymentRepositoryPort
from ....domain.ports.invoice_repository_port import InvoiceRepositoryPort
from ....domain.ports.educacao_service_port import EducacaoServicePort
from ....domain.ports.juventude_service_port import JuventudeServicePort
from ....domain.ports.emprego_service_port import EmpregoServicePort
from ....domain.ports.saude_service_port import SaudeServicePort
from ....domain.ports.assistencia_social_service_port import AssistenciaSocialServicePort
from ....domain.ports.service_requests_service_port import ServiceRequestsServicePort
from ....application.dto.payment_schema import CreatePaymentSchema
from ....domain.exceptions import DuplicatePaymentError, InvoiceNotFoundError, InvalidInvoiceStateError, DomainValidationError
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

    def __init__(self, payment_repository: PaymentRepositoryPort, invoice_repository: InvoiceRepositoryPort, educacao_service: EducacaoServicePort | None=None, juventude_service: JuventudeServicePort | None=None, emprego_service: EmpregoServicePort | None=None, saude_service: SaudeServicePort | None=None, assistencia_social_service: AssistenciaSocialServicePort | None=None, service_requests_service: ServiceRequestsServicePort | None=None):
        self.payment_repo = payment_repository
        self.invoice_repo = invoice_repository
        self._module_adapters = {'educacao': educacao_service, 'juventude': juventude_service, 'emprego': emprego_service, 'saude': saude_service, 'assistencia_social': assistencia_social_service, 'service_requests': service_requests_service}

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
        logger.info(f'Registando pagamento para fatura: {data.invoice_id} (ref: {data.gateway_reference})')
        if await self.payment_repo.exists_by_gateway_ref(data.gateway_reference):
            logger.warning(f'Pagamento duplicado interceptado: {data.gateway_reference}')
            raise DuplicatePaymentError(data.gateway_reference)
        invoice = await self.invoice_repo.get_by_id(data.invoice_id)
        if not invoice:
            logger.error(f'Fatura não encontrada: {data.invoice_id}')
            raise InvoiceNotFoundError(data.invoice_id)
        if round(float(data.amount), 2) != round(float(invoice.amount), 2):
            raise DomainValidationError('Montante do pagamento divergente do valor da fatura')
        if invoice.status == InvoiceStatus.PAID:
            logger.error(f'Tentativa de pagar fatura já liquidada: {invoice.id}')
            raise InvalidInvoiceStateError(current_status=invoice.status.value, action='pagar novamente')
        if invoice.status == InvoiceStatus.CANCELLED:
            logger.error(f'Tentativa de pagar fatura cancelada: {invoice.id}')
            raise InvalidInvoiceStateError(current_status=invoice.status.value, action='processar pagamento')
        payment = Payment(id=str(uuid.uuid4()), invoice_id=data.invoice_id, citizen_id=data.citizen_id, amount=data.amount, currency=data.currency, gateway_reference=data.gateway_reference, payment_method=data.payment_method, status=PaymentStatus.COMPLETED, created_at=datetime.now(timezone.utc), confirmed_at=datetime.now(timezone.utc))
        try:
            invoice.change_status(InvoiceStatus.PAID, reason=f'Liquidado via {data.payment_method} - Ref: {data.gateway_reference}')
            new_payment = await self.payment_repo.create(payment)
            await self.invoice_repo.save(invoice)
            await self._notify_origin_module(invoice, new_payment)
            logger.info(f'Pagamento {new_payment.id} processado. Fatura {invoice.reference} marcada como PAGA')
            return new_payment
        except DomainValidationError as e:
            logger.error(f'Violação de regra: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Falha ao processar pagamento: {str(e)}')
            raise

    @trace()
    async def get_payment_history(self, citizen_id: str) -> List[Payment]:
        """Recupera histórico de pagamentos do cidadão."""
        logger.info(f'Recuperando histórico de pagamentos: {citizen_id}')
        return await self.payment_repo.get_by_citizen(citizen_id)

    @trace()
    async def get_payment_by_reference(self, reference: str) -> Optional[Payment]:
        """Busca pagamento por referência (ideal para reconciliação)."""
        return await self.payment_repo.get_by_gateway_ref(reference)

    @trace()
    async def list_payments_by_invoice(self, invoice_id: str) -> List[Payment]:
        """Lista todos os pagamentos associados a uma fatura."""
        logger.info(f'Recuperando pagamentos da fatura: {invoice_id}')
        return await self.payment_repo.list_by_invoice(invoice_id)

    async def _notify_origin_module(self, invoice, payment: Payment) -> None:
        module_name = self._resolve_module_name(invoice.service_code)
        if module_name is None:
            return
        adapter = self._module_adapters.get(module_name)
        if adapter is None:
            return
        reference_id = self._parse_request_reference(invoice.request_id)
        if reference_id is None:
            logger.info('Callback financeiro ignorado por ausência de referência UUID', extra={'invoice_id': invoice.id, 'service_code': invoice.service_code})
            return
        callback_name = {'educacao': 'registrar_pagamento_propina', 'juventude': 'registrar_pagamento_bolsa', 'emprego': 'registrar_pagamento_salario', 'saude': 'registrar_pagamento_servico', 'assistencia_social': 'registrar_pagamento_beneficio', 'service_requests': 'registrar_pagamento_taxa'}.get(module_name)
        if callback_name is None:
            return
        callback = getattr(adapter, callback_name, None)
        if callback is None:
            return
        try:
            await callback(reference_id, payment.id, float(payment.amount))
        except Exception as exc:
            logger.warning('Falha ao notificar módulo de origem do pagamento', extra={'invoice_id': invoice.id, 'module': module_name, 'error': str(exc)})

    @staticmethod
    def _resolve_module_name(service_code: str | None) -> str | None:
        code = (service_code or '').upper()
        prefix_map = {'EDU_': 'educacao', 'JUV_': 'juventude', 'EMP_': 'emprego', 'SAU_': 'saude', 'ASS_': 'assistencia_social', 'SRV_': 'service_requests', 'REQ_': 'service_requests'}
        for prefix, module_name in prefix_map.items():
            if code.startswith(prefix):
                return module_name
        return None

    @staticmethod
    def _parse_request_reference(request_id: str | None) -> UUID | None:
        if not request_id:
            return None
        try:
            return UUID(str(request_id))
        except (TypeError, ValueError):
            return None
