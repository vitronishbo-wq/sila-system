import uuid
import logging
from datetime import datetime, timezone
from typing import List, Optional

from app.modules.financas.domain.models.invoice import Invoice
from app.modules.financas.domain.models.enums import InvoiceStatus
from app.modules.financas.application.ports.invoice_repository_port import InvoiceRepositoryPort
from app.modules.financas.schemas.invoice_schema import CreateInvoiceSchema
from app.modules.financas.exceptions import (
    InvoiceNotFoundError, 
    InvalidInvoiceStateError, 
    DomainValidationError,
    FUCError
)
from app.modules.financas.integrations.fuc_client import FUCClient

logger = logging.getLogger(__name__)


class InvoiceService:
    """
    Serviço de Orquestração de Faturas (Motor SILA).
    Garante conformidade com normas: Tesouro Nacional + Ficheiro Único do Cidadão (FUC).
    
    REGRAS FINANCEIRAS:
    1. Cidadão deve estar ATIVO no FUC para receber faturas
    2. Montante deve ser > 0 (validado no domínio também)
    3. Status válidos: PENDING → (PAID | CANCELLED | OVERDUE)
    4. PAID e CANCELLED são estados finais (sem transições adicionais)
    """
    
    def __init__(self, repository: InvoiceRepositoryPort):
        self.repository = repository
        self.fuc_client = FUCClient()

    async def create_invoice(self, data: CreateInvoiceSchema) -> Invoice:
        """
        Emite uma nova fatura oficial com validações financeiras.
        
        Precondições:
        - Cidadão ATIVO no FUC
        - Montante > 0
        - Códigos orçamentais válidos
        """
        logger.info(f"Iniciando emissão de fatura para cidadão: {data.citizen_id}")

        # 1. Validação Antecipada (FUC)
        try:
            is_valid = await self.fuc_client.validate_citizen(data.citizen_id)
            if not is_valid:
                logger.warning(f"Emissão negada: Cidadão {data.citizen_id} inválido ou inativo no FUC.")
                raise DomainValidationError(f"Cidadão {data.citizen_id} não habilitado para emissão de faturas.")
        except DomainValidationError:
            raise
        except Exception as e:
            logger.error(f"Falha na integração FUC: {str(e)}")
            raise FUCError("Serviço de validação de identidade indisponível. Tente novamente mais tarde.")

        # 2. GERAR REFERÊNCIA ÚNICA (Conformidade SILA)
        # Formato: SILA-[YYYY]-[SERVICE_CODE]-[HASH_8]
        year = datetime.now(timezone.utc).year
        unique_suffix = str(uuid.uuid4()).split('-')[0].upper()
        reference = f"SILA-{year}-{data.service_code}-{unique_suffix}"

        # 3. CONSTRUIR ENTIDADE (Validações no __post_init__)
        invoice = Invoice(
            id=str(uuid.uuid4()),
            citizen_id=data.citizen_id,
            reference=reference,
            revenue_code=data.revenue_code,
            cost_center=data.cost_center,
            service_code=data.service_code,
            service_name=data.service_name,
            amount=data.amount,
            currency=data.currency,
            due_date=data.due_date,
            request_id=data.request_id,
            status=InvoiceStatus.PENDING,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        # 4. PERSISTÊNCIA
        saved_invoice = await self.repository.create(invoice)
        logger.info(f"Fatura {saved_invoice.reference} emitida: {saved_invoice.id}")
        return saved_invoice

    async def get_invoice(self, invoice_id: str) -> Invoice:
        """Recupera fatura por ID com validação."""
        invoice = await self.repository.get_by_id(invoice_id)
        if not invoice:
            logger.warning(f"Fatura não encontrada: {invoice_id}")
            raise InvoiceNotFoundError(invoice_id)
        return invoice

    async def list_citizen_invoices(self, citizen_id: str) -> List[Invoice]:
        """Lista histórico de faturas de um cidadão."""
        logger.info(f"Recuperando faturas do cidadão: {citizen_id}")
        return await self.repository.get_by_citizen(citizen_id)

    async def cancel_invoice(self, invoice_id: str, reason: str = "Cancelamento administrativo") -> Invoice:
        """
        Cancela fatura com validação de estado.
        
        REGRA: Apenas PENDING ou OVERDUE podem ser canceladas.
        PAID e CANCELLED são estados finais.
        """
        invoice = await self.get_invoice(invoice_id)
        
        # Valida transição (exeção se inválida)
        invoice.change_status(InvoiceStatus.CANCELLED, reason=reason)
        
        updated_invoice = await self.repository.save(invoice)
        logger.info(f"Fatura {invoice_id} cancelada: {reason}")
        return updated_invoice

    async def mark_overdue(self, invoice_id: str) -> Invoice:
        """
        Marca fatura como OVERDUE se data limite ultrapassada.
        
        REGRA: Apenas PENDING → OVERDUE é válido.
        """
        invoice = await self.get_invoice(invoice_id)
        
        if invoice.is_overdue() and invoice.status == InvoiceStatus.PENDING:
            invoice.change_status(
                InvoiceStatus.OVERDUE, 
                reason="Data limite de pagamento ultrapassada"
            )
            updated_invoice = await self.repository.save(invoice)
            logger.info(f"Fatura {invoice_id} marcada como OVERDUE")
            return updated_invoice
        
        return invoice

    async def get_pending_by_citizen(self, citizen_id: str) -> List[Invoice]:
        """Recupera faturas pendentes de um cidadão."""
        invoices = await self.repository.get_pending(citizen_id)
        logger.info(f"Encontradas {len(invoices)} faturas pendentes para: {citizen_id}")
        return invoices
