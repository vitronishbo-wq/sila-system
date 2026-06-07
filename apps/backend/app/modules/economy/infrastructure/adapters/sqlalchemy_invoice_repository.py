from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.models.enums import InvoiceStatus
from ...domain.models.invoice import Invoice
from ...domain.ports.invoice_repository_port import InvoiceRepositoryPort
from ..models import EconomyInvoiceModel


class SQLAlchemyInvoiceRepository(InvoiceRepositoryPort):
    """Adapter: SQLAlchemy implementation of InvoiceRepositoryPort for Economy module."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, invoice: Invoice) -> Invoice:
        """Create a new invoice."""
        model = self._to_model(invoice)
        self.session.add(model)
        await self.session.flush()
        return self._to_domain(model)

    async def save(self, invoice: Invoice) -> Invoice:
        """Save/update an invoice."""
        model = self._to_model(invoice)
        await self.session.merge(model)
        await self.session.flush()
        return self._to_domain(model)

    async def get_by_id(self, invoice_id: str) -> Invoice | None:
        """Get invoice by ID."""
        result = await self.session.execute(
            select(EconomyInvoiceModel).where(EconomyInvoiceModel.id == invoice_id)
        )
        model = result.scalars().first()
        return self._to_domain(model) if model else None

    async def get_by_citizen(self, citizen_id: str) -> list[Invoice]:
        """List invoices for citizen."""
        result = await self.session.execute(
            select(EconomyInvoiceModel)
            .where(EconomyInvoiceModel.citizen_id == citizen_id)
            .order_by(EconomyInvoiceModel.created_at.desc())
        )
        return [self._to_domain(item) for item in result.scalars().all()]

    async def get_pending(self, citizen_id: str) -> list[Invoice]:
        """List pending/overdue invoices for citizen."""
        result = await self.session.execute(
            select(EconomyInvoiceModel)
            .where(
                EconomyInvoiceModel.citizen_id == citizen_id,
                EconomyInvoiceModel.status.in_(
                    [InvoiceStatus.PENDING.value, InvoiceStatus.OVERDUE.value]
                ),
            )
            .order_by(EconomyInvoiceModel.created_at.desc())
        )
        return [self._to_domain(item) for item in result.scalars().all()]

    async def list_all(self, limit: int = 100, offset: int = 0) -> list[Invoice]:
        """List all invoices."""
        result = await self.session.execute(
            select(EconomyInvoiceModel)
            .order_by(EconomyInvoiceModel.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return [self._to_domain(item) for item in result.scalars().all()]

    async def delete(self, invoice_id: str) -> bool:
        """Delete an invoice."""
        result = await self.session.execute(
            delete(EconomyInvoiceModel).where(EconomyInvoiceModel.id == invoice_id)
        )
        await self.session.flush()
        return result.rowcount > 0

    @staticmethod
    def _to_model(invoice: Invoice) -> EconomyInvoiceModel:
        return EconomyInvoiceModel(
            id=invoice.id,
            citizen_id=invoice.citizen_id,
            reference=invoice.reference,
            revenue_code=invoice.revenue_code,
            cost_center=invoice.cost_center,
            service_code=invoice.service_code,
            service_name=invoice.service_name,
            amount=invoice.amount,
            currency=invoice.currency,
            status=invoice.status.value
            if hasattr(invoice.status, "value")
            else str(invoice.status),
            due_date=invoice.due_date,
            request_id=invoice.request_id,
            paid_at=invoice.paid_at,
            created_at=invoice.created_at,
            updated_at=invoice.updated_at,
        )

    @staticmethod
    def _to_domain(model: EconomyInvoiceModel) -> Invoice:
        try:
            status = InvoiceStatus(model.status)
        except Exception:
            status = InvoiceStatus.PENDING
        return Invoice(
            id=model.id,
            citizen_id=model.citizen_id,
            reference=model.reference,
            revenue_code=model.revenue_code,
            cost_center=model.cost_center,
            service_code=model.service_code,
            service_name=model.service_name,
            amount=float(model.amount),
            due_date=model.due_date,
            request_id=model.request_id,
            currency=model.currency,
            status=status,
            created_at=model.created_at,
            updated_at=model.updated_at,
            paid_at=model.paid_at,
        )
