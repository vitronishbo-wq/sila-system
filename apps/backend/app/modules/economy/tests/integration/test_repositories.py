from datetime import datetime, timedelta, timezone
import uuid
import pytest
from app.modules.economy.domain.models.invoice import Invoice
from app.modules.economy.domain.models.payment import Payment
from app.modules.economy.domain.models.enums import InvoiceStatus, PaymentStatus
from app.modules.economy.infrastructure.adapters.sqlalchemy_invoice_repository import SQLAlchemyInvoiceRepository
from app.modules.economy.infrastructure.adapters.sqlalchemy_payment_repository import SQLAlchemyPaymentRepository
from app.modules.economy.core.application.services.payment_service import PaymentService
from app.modules.economy.application.dto.payment_schema import CreatePaymentSchema

class TestRepositories:
    """Repository integration tests"""

    @pytest.mark.asyncio
    async def test_invoice_repository_crud(self, db_session):
        repo = SQLAlchemyInvoiceRepository(db_session)
        now = datetime.now(timezone.utc)
        invoice = Invoice(
            id=str(uuid.uuid4()),
            citizen_id='cit_123',
            reference=f'SILA-TEST-{uuid.uuid4().hex[:6].upper()}',
            revenue_code='4211.08.01',
            cost_center='CC001',
            service_code='SRV_TAXA',
            service_name='Taxa de Serviço',
            amount=1500.0,
            currency='AOA',
            due_date=now + timedelta(days=10),
            status=InvoiceStatus.PENDING,
            created_at=now,
            updated_at=now,
        )
        created = await repo.create(invoice)
        await db_session.commit()

        fetched = await repo.get_by_id(created.id)
        assert fetched is not None
        assert fetched.reference == invoice.reference

        by_citizen = await repo.get_by_citizen('cit_123')
        assert len(by_citizen) == 1

        all_items = await repo.list_all(limit=10, offset=0)
        assert len(all_items) == 1

        deleted = await repo.delete(created.id)
        await db_session.commit()
        assert deleted is True

    @pytest.mark.asyncio
    async def test_payment_repository_crud(self, db_session):
        invoice_repo = SQLAlchemyInvoiceRepository(db_session)
        payment_repo = SQLAlchemyPaymentRepository(db_session)
        now = datetime.now(timezone.utc)
        invoice = Invoice(
            id=str(uuid.uuid4()),
            citizen_id='cit_123',
            reference=f'SILA-TEST-{uuid.uuid4().hex[:6].upper()}',
            revenue_code='4211.08.01',
            cost_center='CC001',
            service_code='SRV_TAXA',
            service_name='Taxa de Serviço',
            amount=3000.0,
            currency='AOA',
            due_date=now + timedelta(days=5),
            status=InvoiceStatus.PENDING,
            created_at=now,
            updated_at=now,
        )
        await invoice_repo.create(invoice)
        await db_session.commit()

        payment = Payment(
            id=str(uuid.uuid4()),
            invoice_id=invoice.id,
            citizen_id=invoice.citizen_id,
            amount=invoice.amount,
            currency=invoice.currency,
            gateway_reference=f'GW-{uuid.uuid4().hex[:8].upper()}',
            payment_method='multicaixa',
            status=PaymentStatus.COMPLETED,
            created_at=now,
            confirmed_at=now,
        )
        created = await payment_repo.create(payment)
        await db_session.commit()

        fetched = await payment_repo.get_by_id(created.id)
        assert fetched is not None
        assert fetched.gateway_reference == payment.gateway_reference

        by_invoice = await payment_repo.list_by_invoice(invoice.id)
        assert len(by_invoice) == 1

        by_citizen = await payment_repo.get_by_citizen(invoice.citizen_id)
        assert len(by_citizen) == 1

class TestApplicationServices:
    """Application service integration tests"""

    @pytest.mark.asyncio
    async def test_payment_service_registers_and_updates_invoice(self, db_session):
        invoice_repo = SQLAlchemyInvoiceRepository(db_session)
        payment_repo = SQLAlchemyPaymentRepository(db_session)
        now = datetime.now(timezone.utc)
        invoice = Invoice(
            id=str(uuid.uuid4()),
            citizen_id='cit_123',
            reference=f'SILA-TEST-{uuid.uuid4().hex[:6].upper()}',
            revenue_code='4211.08.01',
            cost_center='CC001',
            service_code='SRV_TAXA',
            service_name='Taxa de Serviço',
            amount=5000.0,
            currency='AOA',
            due_date=now + timedelta(days=10),
            status=InvoiceStatus.PENDING,
            created_at=now,
            updated_at=now,
        )
        await invoice_repo.create(invoice)
        await db_session.commit()

        service = PaymentService(payment_repo, invoice_repo)
        payload = CreatePaymentSchema(
            invoice_id=invoice.id,
            citizen_id=invoice.citizen_id,
            amount=invoice.amount,
            currency=invoice.currency,
            gateway_reference=f'GW-{uuid.uuid4().hex[:8].upper()}',
            payment_method='multicaixa',
        )
        payment = await service.register_payment(payload)
        await db_session.commit()

        assert payment.id is not None
        updated = await invoice_repo.get_by_id(invoice.id)
        assert updated is not None
        assert updated.status == InvoiceStatus.PAID
