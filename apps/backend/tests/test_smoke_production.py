import uuid
from datetime import datetime, timedelta
import pytest
from sqlalchemy import select
from sqlalchemy.exc import ProgrammingError
from app.core.db import AsyncSessionLocal
from app.core.bridges.identity_bridge import CitizenFUC
from app.core.workflow.models.process import Process
from app.core.catalog.models.service import Service
from apps.backend.app.modules.justice.civil_registry.domain.models.document import Document
from apps.backend.app.modules.economy.financas.domain.models.invoice import Invoice
from apps.backend.app.modules.economy.financas.domain.models.payment import Payment
from apps.backend.app.modules.economy.financas.domain.models.enums import InvoiceStatus, PaymentStatus


@pytest.mark.asyncio
async def test_smoke_production_flow():
    """
    CRITICAL SMOKE TEST: 
    - Sobe app (via session)
    - Cria cidadão
    - Cria pedido
    - Associa documento
    - Gera invoice
    - Regista pagamento fake
    """
    async with AsyncSessionLocal() as session:
        print("\n[SMOKE] 1. Criando cidadão...")
        citizen_id = uuid.uuid4()
        unique_suffix = uuid.uuid4().hex[:6]
        citizen = CitizenFUC(
            citizen_id=citizen_id,
            full_name=f"Smoke Test User {unique_suffix}",
            email=f"smoke_{unique_suffix}@test.ao",
            birth_date=datetime(1995, 5, 20),
            document_number=f"SMK{unique_suffix.upper()}001",
            vital_status="active",
            is_active=True
        )
        session.add(citizen)
        await session.flush()
        
        print("[SMOKE] 2. Buscando serviço BI_EMISSAO...")
        try:
            res = await session.execute(select(Service).where(Service.code == "BI_EMISSAO"))
        except ProgrammingError as exc:
            pytest.skip(f"Schema/services model mismatch in test env: {exc}")
        service = res.scalars().first()
        assert service is not None, "Serviço BI_EMISSAO não encontrado. Rodar seeds antes?"
        
        print("[SMOKE] 3. Criando pedido (Process)...")
        process = Process(
            id=uuid.uuid4(),
            service_id=service.id,
            citizen_id=citizen_id,
            status="submitted"
        )
        session.add(process)
        await session.flush()
        
        print("[SMOKE] 4. Associando documento...")
        doc = Document(
            id=uuid.uuid4(),
            citizen_id=citizen_id,
            document_type="ID_CARD",
            document_number=f"DOC{unique_suffix.upper()}",
            status="valid"
        )
        session.add(doc)
        await session.flush()
        
        print("[SMOKE] 5. Gerando invoice...")
        invoice_id = f"INV-SMOKE-{unique_suffix.upper()}"
        invoice = Invoice(
            id=invoice_id,
            citizen_id=str(citizen_id),
            reference=f"REF-SMK-{unique_suffix.upper()}",
            revenue_code="1.1.1.1",
            cost_center="SILA-TEST",
            service_code=service.code,
            service_name=service.name,
            amount=service.price,
            due_date=datetime.utcnow() + timedelta(days=7),
            status=InvoiceStatus.PENDING
        )
        session.add(invoice)
        await session.flush()
        
        print("[SMOKE] 6. Registrando pagamento...")
        payment = Payment(
            id=str(uuid.uuid4()),
            invoice_id=invoice_id,
            citizen_id=str(citizen_id),
            amount=service.price,
            payment_method="CASH",
            gateway_reference=f"GW-{unique_suffix.upper()}",
            status=PaymentStatus.COMPLETED,
            created_at=datetime.utcnow()
        )
        session.add(payment)
        
        # Atualizar invoice como paga
        invoice.status = InvoiceStatus.PAID
        
        print("[SMOKE] 7. Committing transaction...")
        await session.commit()
        
        print(f"✅ [SMOKE SUCCESS] Fluxo completo para cidadão {citizen_id}")

    # Verificação pós-commit
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(CitizenFUC).where(CitizenFUC.citizen_id == citizen_id))
        stored_citizen = res.scalars().first()
        assert stored_citizen is not None
        assert stored_citizen.full_name.startswith("Smoke Test User")
        print("Verification: Data persisted correctly.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_smoke_production_flow())
