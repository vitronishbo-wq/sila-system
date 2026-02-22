from typing import Optional, List, Tuple
from uuid import UUID
from datetime import date, datetime
import logging

from .taxpayer_service import TaxpayerService
from .tax_declaration_service import TaxDeclarationService
from .tax_debt_service import TaxDebtService
from .tax_certificate_service import TaxCertificateService
from .agt_sync_service import AGTSyncService
from .tax_payment_service import TaxPaymentService
from ..ports.unit_of_work_port import UnitOfWorkPort
from ..ports.event_bus_port import EventBusPort


class TaxpayerApplicationFacade:
    """
    Facade unificado para operações de contribuinte.
    
    Evita service explosion e fornece uma entrada única para a API.
    Gerencia coordenação entre múltiplos services.
    """
    
    def __init__(
        self,
        taxpayer_service: TaxpayerService,
        declaration_service: TaxDeclarationService,
        debt_service: TaxDebtService,
        certificate_service: TaxCertificateService,
        agt_sync_service: AGTSyncService,
        payment_service: TaxPaymentService,
        unit_of_work: UnitOfWorkPort,
        event_bus: EventBusPort
    ):
        self.taxpayer = taxpayer_service
        self.declaration = declaration_service
        self.debt = debt_service
        self.certificate = certificate_service
        self.agt = agt_sync_service
        self.payment = payment_service
        self.uow = unit_of_work
        self.event_bus = event_bus
        self.logger = logging.getLogger(__name__)
    
    # ==================== TAXPAYER OPERATIONS ====================
    
    async def register_taxpayer(
        self,
        nif: str,
        name: str,
        email: Optional[str],
        phone: Optional[str],
        address: Optional[str],
        tax_regime: str,
        registered_by: UUID,
        ip_address: Optional[str] = None
    ):
        """Registra novo contribuinte com transação"""
        async with self.uow:
            taxpayer = await self.taxpayer.register_taxpayer(
                nif, name, email, phone, address, tax_regime, registered_by, ip_address
            )
            await self.uow.commit()
            return taxpayer
    
    async def get_taxpayer(self, taxpayer_id: UUID):
        """Busca contribuinte"""
        return await self.taxpayer.get_taxpayer(taxpayer_id)
    
    async def get_taxpayer_by_nif(self, nif: str):
        """Busca contribuinte por NIF"""
        return await self.taxpayer.get_taxpayer_by_nif(nif)
    
    async def update_taxpayer(
        self,
        taxpayer_id: UUID,
        updates: dict,
        updated_by: UUID,
        ip_address: Optional[str] = None
    ):
        """Atualiza contribuinte com transação"""
        async with self.uow:
            taxpayer = await self.taxpayer.update_taxpayer(
                taxpayer_id, updates, updated_by, ip_address
            )
            await self.uow.commit()
            return taxpayer
    
    async def change_taxpayer_status(
        self,
        taxpayer_id: UUID,
        new_status: str,
        reason: str,
        changed_by: UUID,
        ip_address: Optional[str] = None
    ):
        """Altera status do contribuinte com transação"""
        async with self.uow:
            taxpayer = await self.taxpayer.change_status(
                taxpayer_id, new_status, reason, changed_by, ip_address
            )
            await self.uow.commit()
            return taxpayer
    
    async def list_taxpayers(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        tax_regime: Optional[str] = None,
        search: Optional[str] = None
    ):
        """Lista contribuintes"""
        return await self.taxpayer.list_taxpayers(skip, limit, status, tax_regime, search)
    
    # ==================== DECLARATION OPERATIONS ====================
    
    async def file_declaration(
        self,
        taxpayer_id: UUID,
        tax_type: str,
        tax_period: str,
        gross_amount: float,
        deductions: Optional[float],
        submitted_by: UUID,
        ip_address: Optional[str] = None
    ):
        """Submete declaração com transação"""
        async with self.uow:
            declaration = await self.declaration.submit_declaration(
                taxpayer_id, tax_type, tax_period, gross_amount, deductions, submitted_by, ip_address
            )
            await self.uow.commit()
            return declaration
    
    async def get_declarations(
        self,
        taxpayer_id: UUID,
        year: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ):
        """Lista declarações"""
        return await self.declaration.get_taxpayer_declarations(taxpayer_id, year, skip, limit)
    
    async def process_declaration(
        self,
        declaration_id: UUID,
        status: str,
        processed_by: UUID,
        observations: Optional[str] = None,
        ip_address: Optional[str] = None
    ):
        """Processa declaração (aprova/rejeita) com transação"""
        async with self.uow:
            declaration = await self.declaration.process_declaration(
                declaration_id, status, processed_by, observations, ip_address
            )
            await self.uow.commit()
            return declaration
    
    # ==================== DEBT OPERATIONS ====================
    
    async def create_debt(
        self,
        taxpayer_id: UUID,
        tax_type: str,
        original_amount: float,
        due_date: date,
        created_by: UUID,
        description: Optional[str] = None,
        ip_address: Optional[str] = None
    ):
        """Cria dívida com transação"""
        async with self.uow:
            debt = await self.debt.create_debt(
                taxpayer_id, tax_type, original_amount, due_date, created_by, description, ip_address
            )
            await self.uow.commit()
            return debt
    
    async def get_debts(
        self,
        taxpayer_id: UUID,
        include_paid: bool = False,
        skip: int = 0,
        limit: int = 100
    ):
        """Lista dívidas"""
        return await self.debt.get_taxpayer_debts(taxpayer_id, include_paid, skip, limit)
    
    async def register_debt_payment(
        self,
        debt_id: UUID,
        amount: float,
        payment_method: str,
        payment_date: datetime,
        paid_by: UUID,
        reference: Optional[str] = None,
        ip_address: Optional[str] = None
    ):
        """Registra pagamento de dívida com transação"""
        async with self.uow:
            payment = await self.debt.register_payment(
                debt_id, amount, payment_method, payment_date, paid_by, reference, ip_address
            )
            await self.uow.commit()
            return payment
    
    # ==================== CERTIFICATE OPERATIONS ====================
    
    async def request_certificate(
        self,
        taxpayer_id: UUID,
        certificate_type: str,
        year: Optional[int],
        requested_by: UUID,
        purpose: Optional[str] = None,
        ip_address: Optional[str] = None
    ):
        """Solicita certidão com transação"""
        async with self.uow:
            certificate = await self.certificate.request_certificate(
                taxpayer_id, certificate_type, year, requested_by, purpose, ip_address
            )
            await self.uow.commit()
            return certificate
    
    async def get_certificates(
        self,
        taxpayer_id: UUID,
        certificate_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ):
        """Lista certidões"""
        return await self.certificate.get_taxpayer_certificates(
            taxpayer_id, certificate_type, skip, limit
        )
    
    async def process_certificate(
        self,
        certificate_id: UUID,
        status: str,
        processed_by: UUID,
        file_url: Optional[str] = None,
        ip_address: Optional[str] = None
    ):
        """Processa certidão (emite/rejeita) com transação"""
        async with self.uow:
            certificate = await self.certificate.process_certificate(
                certificate_id, status, processed_by, file_url, ip_address
            )
            await self.uow.commit()
            return certificate
    
    # ==================== PAYMENT OPERATIONS ====================
    
    async def process_payment(
        self,
        taxpayer_id: UUID,
        amount: float,
        payment_method: str,
        paid_by: UUID,
        debt_ids: Optional[List[UUID]] = None,
        reference: Optional[str] = None,
        metadata: Optional[dict] = None,
        ip_address: Optional[str] = None
    ):
        """Processa pagamento de um ou múltiplos débitos com transação"""
        async with self.uow:
            payments = await self.payment.process_payment(
                taxpayer_id, amount, payment_method, paid_by, debt_ids, reference, metadata, ip_address
            )
            await self.uow.commit()
            return payments
    
    async def get_payments(
        self,
        taxpayer_id: UUID,
        skip: int = 0,
        limit: int = 100
    ):
        """Lista pagamentos"""
        return await self.payment.get_taxpayer_payments(taxpayer_id, skip, limit)
    
    async def reverse_payment(
        self,
        payment_id: UUID,
        reason: str,
        reversed_by: UUID,
        ip_address: Optional[str] = None
    ):
        """Estorna pagamento com transação"""
        async with self.uow:
            payment = await self.payment.reverse_payment(
                payment_id, reason, reversed_by, ip_address
            )
            await self.uow.commit()
            return payment
    
    # ==================== SYNCHRONIZATION ====================
    
    async def sync_with_agt(self, taxpayer_id: UUID):
        """Sincroniza contribuinte com AGT (single taxpayer)"""
        async with self.uow:
            result = await self.agt.sync_taxpayer(taxpayer_id)
            await self.uow.commit()
            return result
    
    async def sync_all_with_agt(self, batch_size: int = 100):
        """Sincroniza todos os contribuintes com AGT (batch)"""
        async with self.uow:
            result = await self.agt.sync_all_taxpayers(batch_size)
            await self.uow.commit()
            return result
    
    async def check_agt_health(self):
        """Verifica saúde da integração com AGT"""
        return await self.agt.check_agt_health()
