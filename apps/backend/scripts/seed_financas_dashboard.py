from __future__ import annotations

import asyncio
import os
import uuid
from datetime import UTC, datetime, timedelta

from apps.backend.app.core.db import AsyncSessionLocal
from apps.backend.app.modules.economy.application.dto.payment_schema import CreatePaymentSchema
from apps.backend.app.modules.economy.core.application.services.payment_service import PaymentService
from apps.backend.app.modules.economy.domain.models.enums import InvoiceStatus
from apps.backend.app.modules.economy.domain.models.invoice import Invoice
from apps.backend.app.modules.economy.infrastructure.adapters import (
    SQLAlchemyInvoiceRepository,
    SQLAlchemyPaymentRepository,
)
from sqlalchemy import text


async def seed_financas_dashboard() -> None:
    citizen_id = os.getenv("FINANCAS_DEMO_CITIZEN_ID", "cit_123")
    now = datetime.now(UTC)

    async with AsyncSessionLocal() as session:
        count = (await session.execute(text("SELECT COUNT(*) FROM economy_invoices"))).scalar_one()
        if count > 0:
            print("Economy invoices already seeded. Skipping.")
            return

        invoice_repo = SQLAlchemyInvoiceRepository(session)
        payment_repo = SQLAlchemyPaymentRepository(session)
        payment_service = PaymentService(payment_repo, invoice_repo)

        invoices = [
            Invoice(
                id=str(uuid.uuid4()),
                citizen_id=citizen_id,
                reference=f"SILA-DEMO-{uuid.uuid4().hex[:6].upper()}",
                revenue_code="4211.08.01",
                cost_center="CC001",
                service_code="SRV_TAXA",
                service_name="Taxa de Pedido de Serviço",
                amount=1500.0,
                currency="AOA",
                due_date=now + timedelta(days=10),
                status=InvoiceStatus.PENDING,
                created_at=now,
                updated_at=now,
            ),
            Invoice(
                id=str(uuid.uuid4()),
                citizen_id=citizen_id,
                reference=f"SILA-DEMO-{uuid.uuid4().hex[:6].upper()}",
                revenue_code="4211.08.01",
                cost_center="CC002",
                service_code="EDU_PROPINA",
                service_name="Propina Escolar",
                amount=3200.0,
                currency="AOA",
                due_date=now - timedelta(days=2),
                status=InvoiceStatus.OVERDUE,
                created_at=now - timedelta(days=15),
                updated_at=now - timedelta(days=2),
            ),
            Invoice(
                id=str(uuid.uuid4()),
                citizen_id=citizen_id,
                reference=f"SILA-DEMO-{uuid.uuid4().hex[:6].upper()}",
                revenue_code="4211.08.01",
                cost_center="CC003",
                service_code="SAU_TAXA",
                service_name="Taxa de Serviço de Saúde",
                amount=4800.0,
                currency="AOA",
                due_date=now + timedelta(days=5),
                status=InvoiceStatus.PENDING,
                created_at=now - timedelta(days=1),
                updated_at=now - timedelta(days=1),
            ),
        ]

        for invoice in invoices:
            await invoice_repo.create(invoice)
        await session.commit()

        payment_payload = CreatePaymentSchema(
            invoice_id=invoices[2].id,
            citizen_id=citizen_id,
            amount=invoices[2].amount,
            currency=invoices[2].currency,
            gateway_reference=f"GW-DEMO-{uuid.uuid4().hex[:8].upper()}",
            payment_method="multicaixa",
        )
        await payment_service.register_payment(payment_payload)
        await session.commit()

        print("✅ Seed de finanças concluído com sucesso.")


if __name__ == "__main__":
    asyncio.run(seed_financas_dashboard())
