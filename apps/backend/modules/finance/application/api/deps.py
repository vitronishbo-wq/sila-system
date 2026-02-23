from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.modules.financas.application.services.invoice_service import InvoiceService
from app.modules.financas.application.services.payment_service import PaymentService
from app.modules.financas.infrastructure.repositories.invoice_repository import InvoiceRepository
from app.modules.financas.infrastructure.repositories.payment_repository import PaymentRepository

async def get_invoice_repository(db: AsyncSession = Depends(get_db)) -> InvoiceRepository:
    return InvoiceRepository(db)

async def get_payment_repository(db: AsyncSession = Depends(get_db)) -> PaymentRepository:
    return PaymentRepository(db)

async def get_invoice_service(
    repo: InvoiceRepository = Depends(get_invoice_repository)
) -> InvoiceService:
    return InvoiceService(repo)

async def get_payment_service(
    payment_repo: PaymentRepository = Depends(get_payment_repository),
    invoice_repo: InvoiceRepository = Depends(get_invoice_repository)
) -> PaymentService:
    return PaymentService(payment_repo, invoice_repo)
